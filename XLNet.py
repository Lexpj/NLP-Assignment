from transformers import XLNetForCausalLM, XLNetTokenizer

class XLNet:
    
    def __init__(self):
        self.model = XLNetForCausalLM.from_pretrained("xlnet-base-cased")
        self.tok = XLNetTokenizer.from_pretrained("xlnet-base-cased")
    
    def gen(self,sentence, rhymeword):
        
        example_english_phrase = sentence + " <mask> " + rhymeword
        batch = self.tok(example_english_phrase, return_tensors="pt")
        generated_ids = self.model.generate(batch["input_ids"], attention_mask=batch["attention_mask"], max_length=batch["input_ids"].shape[-1])
        res = self.tok.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(res)
        return(res)