def projection_difference(file_one, file_two):
    '''
    Compare two files generated by different translator and/or word aligner

    file_one, file_two: files with different translation/projection methods 

    returns the lines that are different
    '''

    file1 = open(file_one)
    file2 = open(file_two)
    tags_from_first = []
    sequence_one_tags = []
    
    tags_from_second = []
    sequence_two_tags = []
    
    tokens_from_first = []
    sequence_one_tokens = []

    tokens_from_second = []
    sequence_two_tokens  = []
    for first in file1:
        if first != '\n':       
            # print(one)
            sequence_one_tags.append(first.split(' ')[1])
            sequence_one_tokens.append(first.split(' ')[0])
        elif first == '\n':
            tokens_from_first.append(sequence_one_tokens)
            tags_from_first.append(sequence_one_tags)
            sequence_one_tags, sequence_one_tokens = [], []
            
    for second in file2:
        if second != '\n':
            # print(two)
            sequence_two_tags.append(second.split(' ')[1])
            sequence_two_tokens.append(second.split(' ')[0])
        elif second == '\n':
            tokens_from_second.append(sequence_two_tokens)
            tags_from_second.append(sequence_two_tags)
            sequence_two_tags, sequence_two_tokens = [], []
        # break

    print('Tags: ', len(tags_from_first), len(tags_from_second))
    print('Tokens: ', len(tokens_from_first), len(tokens_from_second))
    assert len(tokens_from_first) == len(tokens_from_second)

    count_tags = 0
    for tag_one, tag_two in zip(tags_from_first, tags_from_second):
        if set(tag_one) != set(tag_two):
            print(tag_one, '\n',tag_two, '\n')
            print(len(tag_one), len(tag_two))
            print('\n') 
            count_tags += 1
    # q = open('/Users/anaryegen/Desktop/projections.txt', 'w')
    # for tag_one, tag_two in zip(tokens_from_first, tokens_from_second):

    #     if set(tag_one) != set(tag_two):
    #         q.write('\n')
    #         q.write(' '.join(tag_one))
    #         q.write('\n')
    #         q.write(' '.join(tag_two))
    #         # print(len(tag_one), len(tag_two))
    #         q.write('\n')
    # #         # count_tags += 

    count_tokens = 0
    for token_one, token_two in zip(tokens_from_first, tokens_from_second):
        if token_one != token_two:
            # print(token_one, '\n',token_two)
            # print(len(token_one), len(token_two))
            # print('\n') 
            count_tokens += 1
    print("Difference in projection: ", count_tags)
    # print()
    # print("Difference in translation: ", count_tokens)

projection_difference('/Users/anaryegen/Desktop/AbstRCT-projections/datasets/fr/nllb200/fr-mixed-test.tsv', '/Users/anaryegen/Desktop/AbstRCT-projections/datasets/en/en-mixed-test.tsv')
