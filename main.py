# main.py
from fastapi import FastAPI, Query, Depends, HTTPException
from database import get_db, SpellCheckResult
from models import InputTerm, SpellCheckResponse
from symspellpy import SymSpell, Verbosity
from sqlalchemy.orm import Session
# Initialize the SymSpell instance and load the dictionary
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = "C:\\Users\\apathan\\Desktop\\API\\frequency_dictionary_en_82_765.txt"
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

app = FastAPI()

# Spell check and correction endpoint with query parameter
@app.get("/spellcheck/", response_model=SpellCheckResponse)
def spell_check(term: str = Query(..., title="Input Term"), db: Session = Depends(get_db)):
    suggestions = sym_spell.lookup(term, Verbosity.CLOSEST, max_edit_distance=2,transfer_casing=True, ignore_token=r"\w+\d")
    corrected_terms = [suggestion.term for suggestion in suggestions]

    # Store the result in the database
    db_result = SpellCheckResult(input_term=term, corrections=", ".join(corrected_terms))
    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return SpellCheckResponse(input_term=term, corrections=corrected_terms)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
