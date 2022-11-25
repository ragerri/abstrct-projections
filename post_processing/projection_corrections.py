import argparse 

def read_file(file):
    f = open(file, 'r')
    tokens = []
    tags = []
    current_token = []
    current_tag = []
    for line in f:
        if line != '\n':
            token, tag = line.split()
            current_tag.append(tag)
            current_token.append(token)

        if line == '\n':
            tokens.append(current_token)
            tags.append(current_tag)
            current_tag = []
            current_token = []
    # print(len(tokens), len(tags))
    return tokens, tags

def write_file(source_path, target_path, output_path):
    count = 0
    output = open(output_path, 'w')
    source_token_list, source_tag_list = read_file(source_path)
    target_token_list, target_tag_list = read_file(target_path)
    
    assert len(source_token_list) == len(target_token_list), "Source and target should have equal amount of data/lines"

    for i, s_tag in enumerate(source_tag_list):
        if len(s_tag) > 0 and s_tag[0] != 'O':
            _, tag_type = s_tag[0].split('-')
            
        if len(s_tag) > 1 and s_tag[0].startswith('B') and len(set(s_tag[1:])) == 1:
                
                target_tag_list[i][0] = 'B-'+tag_type
                target_tag_list[i][1:] = ['I-'+tag_type] * len(target_tag_list[i][1:])   
                count += 1

        elif len(s_tag) > 1 and len(set(s_tag)) <= 2 \
        and s_tag[0].startswith('B') and s_tag[-1].startswith('I') \
        and s_tag[0].split('-')[1] == s_tag[-1].split('-')[1]:
            # print(s_tag[0], i)
            
            target_tag_list[i][0] = 'B-'+tag_type
            for t in range(1,len(target_tag_list[i][1:4])):
                # print(t[0])
                if target_tag_list[i][t].startswith('B'):
                    target_tag_list[i][t] = 'I-' + tag_type
                else:
                    target_tag_list[i][1] = 'I-' + tag_type
            
            # target_tag_list[i][1:] = ['I-'+tag_type] * len(target_tag_list[i][1:])
            count += 1
    print("Number of full components: ", count)
    for token, tag in zip(target_token_list, target_tag_list):
        for tkn, tg in zip(token,tag):
            # print(tkn, tg)
            output.write(tkn+ " " +tg + '\n')
        output.write('\n')

def get_numbers(source_file, target_file, output_file):
    source_tokens, source_tags = read_file(source_file)
    target_tokens, target_tags = read_file(target_file)
    output_tokens, output_tags = read_file(output_file)
    c = 0
    for target, output in zip(target_tags, output_tags):
        if target != output:
            c += 1
            # print(target, '\n', output, '\n')
    print("Number of corrections: ", c)
    

    print("Number of sentences: ", len(target_tags))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source_path",
        type=str,
        required=True,
        help="Path to the original version of data in IOB2 format",
    )
    parser.add_argument(
        "--target_path",
        type=str,
        required=True,
        help="Path to the projected data you want to fix in IOB2 format",
    )

    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="File to save the results",
    )


    args = parser.parse_args()

    write_file(
        source_path=args.source_path,
        target_path=args.target_path,
        output_path=args.output_path
    )
    get_numbers(source_file=args.source_path,
        target_file=args.target_path, output_file=args.output_path)
