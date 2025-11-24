import numpy as np
import faiss
from backend.utils import EMBEDDINGS_NPY, FAISS_INDEX

def main():
    vectors = np.load(EMBEDDINGS_NPY)
    dim = vectors.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    faiss.write_index(index, str(FAISS_INDEX))
    print("FAISS index saved →", FAISS_INDEX)

if __name__ == "__main__":
    main()
