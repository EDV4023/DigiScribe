The objective of this engineering project was to design and evaluate a software system that
improves the semantic accuracy of text extracted from handwritten and printed documents.
Conventional Optical Character Recognition ( OCR ) systems frequently fail to accurately interpret
complex or highly cursive handwriting, resulting in unreadable or misleading output. To address
this problem, I engineered and developed a web - based application called DigiScribe which uses an
agentic AI framework. The system preprocesses uploaded images by reducing noise, performs initial
text extraction using traditional OCR techniques, and assigns confidence scores to recognized text
segments. Next step is a context - aware refinement pipeline which selectively improves low -
confidence segments by incorporating user - defined contextual information and character - level
constraints which are optional, while preserving the original text order and high - confidence
outputs. System performance was evaluated by comparing unrefined OCR outputs with context - refined
outputs across multiple test samples. Evaluation criteria included OCR confidence scores and human
readability assessments. The engineered system consistently produced more accurate and readable
text, particularly in regions containing ambiguous handwriting. Importantly, high - confidence
segments remained unchanged, ensuring stability and minimizing unintended modifications. This
project demonstrates that an agentic, context - aware refinement architecture can significantly
enhance OCR performance. The resulting system has practical applications in document digitization,
educational material preservation, and accessibility of handwritten content. The modular design of
the system allows for future extension and optimization.
