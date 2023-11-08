import torch
import numpy as np
from torch import nn
from transformers.modeling_bert import BertPreTrainedModel, BertModel
from torchcrf import CRF
from torch.nn import CrossEntropyLoss


class BertForSequenceTagging(BertPreTrainedModel):

    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels

        self.bert = BertModel(config)

        self.rnn = nn.GRU(config.hidden_size, config.hidden_size, batch_first=True, bidirectional=True)
        #self.rnn = nn.LSTM(config.hidden_size, config.hidden_size, batch_first=True, bidirectional=True)

        self.crf = CRF(config.num_labels, batch_first=True)
        self.classifier = nn.Linear(2 * config.hidden_size, config.num_labels)

        self.init_weights()

    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        labels=None,
    ):

        outputs = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
        )

        sequence_output = outputs[0]

        rnn_out, _ = self.rnn(sequence_output)
        emissions = self.classifier(rnn_out)

        if labels is not None:
            loss = self.crf(emissions, labels)

            path = self.crf.decode(emissions)
            path = torch.LongTensor(path)

            return (-1*loss, emissions, path)
        else:
            path = self.crf.decode(emissions)
            path = torch.LongTensor(path)

            return path


class BertForMultipleChoiceRC(BertPreTrainedModel):

    def __init__(self, config):
        super().__init__(config)

        # encoder
        self.bert = BertModel(config)

        # multiple choice
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.classifier = nn.Linear(config.hidden_size, 1)

        # relation classification
        self.dropout2 = nn.Dropout(config.hidden_dropout_prob)
        self.classifier2 = nn.Linear(config.hidden_size, 2)

        self.init_weights()

    def forward(self, input_ids, token_type_ids=None, attention_mask=None, labels=None, task=None):

        if len(input_ids) == 2 and task is not None:

            input_ids, input_ids_rel = input_ids
            token_type_ids, token_type_ids_rel = token_type_ids
            attention_mask, attention_mask_rel = attention_mask
            labels, labels_rel = labels

            # relation classification (required only for training)
            _, pooled_output_rel = self.bert(input_ids_rel, token_type_ids_rel, attention_mask_rel)
            pooled_output_rel = self.dropout2(pooled_output_rel)
            logits_rel = self.classifier2(pooled_output_rel)

        num_choices = input_ids.shape[1]


        flat_input_ids = input_ids.view(-1, input_ids.size(-1))
        flat_token_type_ids = token_type_ids.view(-1, token_type_ids.size(-1)) if token_type_ids is not None else None
        flat_attention_mask = attention_mask.view(-1, attention_mask.size(-1)) if attention_mask is not None else None

        _, pooled_output_mc = self.bert(flat_input_ids, flat_token_type_ids, flat_attention_mask)
        pooled_output_mc = self.dropout(pooled_output_mc)
        logits = self.classifier(pooled_output_mc)
        reshaped_logits = logits.view(-1, num_choices)

        if labels is not None:

            loss_fct = CrossEntropyLoss()

            if task == "multiplechoice":
                loss = loss_fct(reshaped_logits, labels[:, 0])

            elif task == "relationclassification":
                loss = loss_fct(logits_rel, labels_rel)

            return loss, reshaped_logits, logits_rel

        else:

            mc_preds = np.argmax(reshaped_logits, axis=1).flatten()
            input_ids_rel = []
            token_type_ids_rel = []
            attention_mask_rel = []
            for i, pred in enumerate(mc_preds):
                input_ids_rel.append(input_ids[i][pred].unsqueeze(0))
                token_type_ids_rel.append(token_type_ids[i][pred].unsqueeze(0))
                attention_mask_rel.append(attention_mask[i][pred].unsqueeze(0))

            input_ids_rel = torch.cat(input_ids_rel)
            token_type_ids_rel = torch.cat(token_type_ids_rel)
            attention_mask_rel = torch.cat(attention_mask_rel)

            # relation classification
            _, pooled_output_rel = self.bert(input_ids_rel, token_type_ids_rel, attention_mask_rel)
            pooled_output_rel = self.dropout2(pooled_output_rel)
            logits_rel = self.classifier2(pooled_output_rel)

            return logits_rel, reshaped_logits
