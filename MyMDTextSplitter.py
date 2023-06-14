from langchain.text_splitter import MarkdownTextSplitter
from langchain.docstore.document import Document
import string
class MyMDTextSplitter(MarkdownTextSplitter):
    def  __init__(self, **kwargs):
        super().__init__(**kwargs)

    def split_text(self, text: str):
        """Split incoming text and return chunks."""
        final_chunks = []
        # Get appropriate separator to cs324
        separator = self._separators[-1]
        for _s in self._separators:
            if _s == "":
                separator = _s
                break
            if _s in text:
                separator = _s
                break
        # Now that we have the separator, split the text
        if separator:
            splits = text.split(separator)
        else:
            splits = list(text)
        # Now go merging things, recursively splitting longer texts.
        final_titles = []
        _titles = []
        _good_splits = []
        for s in splits:
            title = s.split('\n')[0]
            title = '-'.join(title.translate(str.maketrans('', '', string.punctuation)).lower().split())
            if self._length_function(s) < self._chunk_size:
                _good_splits.append(s)
                _titles.append(title)
            else:
                if _good_splits:
                    merged_text = self._merge_splits(_good_splits, separator)
                    final_chunks.extend(merged_text)
                    _titles = [mt.split('\n')[0] for mt in merged_text]
                    final_titles.extend(['-'.join(t.translate(str.maketrans(
                        '', '', string.punctuation)).lower().split()) for t in _titles])
                    _good_splits = []
                    _titles = []
                other_info, other_titles = self.split_text(s)
                final_chunks.extend(other_info)
                final_titles.extend(other_titles)
        if _good_splits:
            merged_text = self._merge_splits(_good_splits, separator)
            final_chunks.extend(merged_text)
            final_titles.extend(_titles)

        return final_chunks, final_titles

    def create_documents(
        self, texts, metadatas=None
    ):
        """Create documents from a list of texts."""
        _metadatas = metadatas or [{}] * len(texts)
        documents = []
        for i, text in enumerate(texts):
            if metadatas[i].get('file', '') != 'table':
                link_home = "https://stanford-cs324.github.io/winter2022/lectures/"
            else :
                link_home = "https://github.com/Hannibal046/Awesome-LLM/blob/main/README.md#milestone-papers"
            chunks, titles = self.split_text(text)
            ct = zip(chunks, titles)
            for chunk, title in ct:
                new_doc = Document(
                    page_content=chunk,
                    metadata={
                        'reference': link_home + metadatas[i].get('file', '') + title})
                documents.append(new_doc)
        return documents

if __name__ == "__main__":
    splitter = MyMDTextSplitter()
    with open('data/cs324/introduction.md') as f:
        text = f.read()
    docs = splitter.create_documents([text],[{'file': 'introduction'}])
    print(docs)