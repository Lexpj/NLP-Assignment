from transformers import BartForConditionalGeneration, BartTokenizer

def BART(sentence, rhymeword):
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large", forced_bos_token_id=0)
    tok = BartTokenizer.from_pretrained("facebook/bart-large")

    example_english_phrase = sentence + " <mask> " + rhymeword
    batch = tok(example_english_phrase, return_tensors="pt")
    generated_ids = model.generate(batch["input_ids"])

    return(tok.batch_decode(generated_ids, skip_special_tokens=True)[0])

print(type(BART("I want to try this.", "bliss")))