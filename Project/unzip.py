import gzip
import shutil

with gzip.open("emar.csv.gz", "rb") as f_in:
    with open("emar.csv", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)