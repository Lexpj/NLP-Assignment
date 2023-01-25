from transformers import BertModel, BertTokenizer
import torch

# Load the BERT model and tokenizer
model = BertModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def simmy(sentence1, sentence2):

    # Encode the two sentences
    #sentence1 = "This is the first sentence."
    #sentence2 = "This is the second sentence."
    encoded_inputs = tokenizer.encode_plus(sentence1, sentence2, return_tensors='pt')

    # Prepare the input for the BERT model
    input_ids = torch.cat([encoded_inputs['input_ids'], encoded_inputs['input_ids']], dim=-1)
    segment_ids = torch.cat([encoded_inputs['token_type_ids'], encoded_inputs['token_type_ids']], dim=-1)
    attention_mask = torch.cat([encoded_inputs['attention_mask'], encoded_inputs['attention_mask']], dim=-1)

    # Generate embeddings for the two sentences
    embeddings = model(input_ids, attention_mask=attention_mask, token_type_ids=segment_ids)[0]

    # Compute the cosine similarity between the embeddings
    sentence1_embedding = embeddings[:, 0, :]
    sentence2_embedding = embeddings[:, 1, :]
    similarity = torch.nn.CosineSimilarity(dim=1)(sentence1_embedding, sentence2_embedding)
    similarity_score = similarity.item()

    print("Similarity score: ", similarity_score)
    return(similarity_score)

simmy('My dog stepped on a bee', 'He stepped on a tree')

