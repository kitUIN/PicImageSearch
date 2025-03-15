"""
This type stub file was generated by pyright.
"""

import difflib

__all__ = ['html_annotate', 'htmldiff']
_unicode = ...
def default_markup(text, version): # -> str:
    ...

def html_annotate(doclist, markup=...): # -> LiteralString:
    """
    doclist should be ordered from oldest to newest, like::

        >>> version1 = 'Hello World'
        >>> version2 = 'Goodbye World'
        >>> print(html_annotate([(version1, 'version 1'),
        ...                      (version2, 'version 2')]))
        <span title="version 2">Goodbye</span> <span title="version 1">World</span>

    The documents must be *fragments* (str/UTF8 or unicode), not
    complete documents

    The markup argument is a function to markup the spans of words.
    This function is called like markup('Hello', 'version 2'), and
    returns HTML.  The first argument is text and never includes any
    markup.  The default uses a span with a title:

        >>> print(default_markup('Some Text', 'by Joe'))
        <span title="by Joe">Some Text</span>
    """
    ...

def tokenize_annotated(doc, annotation): # -> list[token | Any] | list[Any]:
    """Tokenize a document and add an annotation attribute to each token
    """
    ...

def html_annotate_merge_annotations(tokens_old, tokens_new): # -> None:
    """Merge the annotations from tokens_old into tokens_new, when the
    tokens in the new document already existed in the old document.
    """
    ...

def copy_annotations(src, dest): # -> None:
    """
    Copy annotations from the tokens listed in src to the tokens in dest
    """
    ...

def compress_tokens(tokens): # -> list[Any]:
    """
    Combine adjacent tokens when there is no HTML between the tokens, 
    and they share an annotation
    """
    ...

def compress_merge_back(tokens, tok): # -> None:
    """ Merge tok into the last element of tokens (modifying the list of
    tokens in-place).  """
    ...

def markup_serialize_tokens(tokens, markup_func): # -> Generator[Any, Any, None]:
    """
    Serialize the list of tokens into a list of text chunks, calling
    markup_func around text to add annotations.
    """
    ...

def htmldiff(old_html, new_html):
    """ Do a diff of the old and new document.  The documents are HTML
    *fragments* (str/UTF8 or unicode), they are not complete documents
    (i.e., no <html> tag).

    Returns HTML with <ins> and <del> tags added around the
    appropriate text.  

    Markup is generally ignored, with the markup from new_html
    preserved, and possibly some markup from old_html (though it is
    considered acceptable to lose some of the old markup).  Only the
    words in the HTML are diffed.  The exception is <img> tags, which
    are treated like words, and the href attribute of <a> tags, which
    are noted inside the tag itself when there are changes.
    """
    ...

def htmldiff_tokens(html1_tokens, html2_tokens): # -> list[Any]:
    """ Does a diff on the tokens themselves, returning a list of text
    chunks (not tokens).
    """
    ...

def expand_tokens(tokens, equal=...): # -> Generator[Any, Any, None]:
    """Given a list of tokens, return a generator of the chunks of
    text for the data in the tokens.
    """
    ...

def merge_insert(ins_chunks, doc): # -> None:
    """ doc is the already-handled document (as a list of text chunks);
    here we add <ins>ins_chunks</ins> to the end of that.  """
    ...

class DEL_START:
    ...


class DEL_END:
    ...


class NoDeletes(Exception):
    """ Raised when the document no longer contains any pending deletes
    (DEL_START/DEL_END) """
    ...


def merge_delete(del_chunks, doc): # -> None:
    """ Adds the text chunks in del_chunks to the document doc (another
    list of text chunks) with marker to show it is a delete.
    cleanup_delete later resolves these markers into <del> tags."""
    ...

def cleanup_delete(chunks):
    """ Cleans up any DEL_START/DEL_END markers in the document, replacing
    them with <del></del>.  To do this while keeping the document
    valid, it may need to drop some tags (either start or end tags).

    It may also move the del into adjacent tags to try to move it to a
    similar location where it was originally located (e.g., moving a
    delete into preceding <div> tag, if the del looks like (DEL_START,
    'Text</div>', DEL_END)"""
    ...

def split_unbalanced(chunks): # -> tuple[list[Any], list[Any], list[Any]]:
    """Return (unbalanced_start, balanced, unbalanced_end), where each is
    a list of text and tag chunks.

    unbalanced_start is a list of all the tags that are opened, but
    not closed in this span.  Similarly, unbalanced_end is a list of
    tags that are closed but were not opened.  Extracting these might
    mean some reordering of the chunks."""
    ...

def split_delete(chunks): # -> tuple[Any, Any, Any]:
    """ Returns (stuff_before_DEL_START, stuff_inside_DEL_START_END,
    stuff_after_DEL_END).  Returns the first case found (there may be
    more DEL_STARTs in stuff_after_DEL_END).  Raises NoDeletes if
    there's no DEL_START found. """
    ...

def locate_unbalanced_start(unbalanced_start, pre_delete, post_delete): # -> None:
    """ pre_delete and post_delete implicitly point to a place in the
    document (where the two were split).  This moves that point (by
    popping items from one and pushing them onto the other).  It moves
    the point to try to find a place where unbalanced_start applies.

    As an example::

        >>> unbalanced_start = ['<div>']
        >>> doc = ['<p>', 'Text', '</p>', '<div>', 'More Text', '</div>']
        >>> pre, post = doc[:3], doc[3:]
        >>> pre, post
        (['<p>', 'Text', '</p>'], ['<div>', 'More Text', '</div>'])
        >>> locate_unbalanced_start(unbalanced_start, pre, post)
        >>> pre, post
        (['<p>', 'Text', '</p>', '<div>'], ['More Text', '</div>'])

    As you can see, we moved the point so that the dangling <div> that
    we found will be effectively replaced by the div in the original
    document.  If this doesn't work out, we just throw away
    unbalanced_start without doing anything.
    """
    ...

def locate_unbalanced_end(unbalanced_end, pre_delete, post_delete): # -> None:
    """ like locate_unbalanced_start, except handling end tags and
    possibly moving the point earlier in the document.  """
    ...

class token(_unicode):
    """ Represents a diffable token, generally a word that is displayed to
    the user.  Opening tags are attached to this token when they are
    adjacent (pre_tags) and closing tags that follow the word
    (post_tags).  Some exceptions occur when there are empty tags
    adjacent to a word, so there may be close tags in pre_tags, or
    open tags in post_tags.

    We also keep track of whether the word was originally followed by
    whitespace, even though we do not want to treat the word as
    equivalent to a similar word that does not have a trailing
    space."""
    hide_when_equal = ...
    def __new__(cls, text, pre_tags=..., post_tags=..., trailing_whitespace=...): # -> Self:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def html(self): # -> str:
        ...
    


class tag_token(token):
    """ Represents a token that is actually a tag.  Currently this is just
    the <img> tag, which takes up visible space just like a word but
    is only represented in a document by a tag.  """
    def __new__(cls, tag, data, html_repr, pre_tags=..., post_tags=..., trailing_whitespace=...): # -> Self:
        ...
    
    def __repr__(self): # -> LiteralString:
        ...
    
    def html(self):
        ...
    


class href_token(token):
    """ Represents the href in an anchor tag.  Unlike other words, we only
    show the href when it changes.  """
    hide_when_equal = ...
    def html(self): # -> LiteralString:
        ...
    


def tokenize(html, include_hrefs=...): # -> list[token | Any] | list[Any]:
    """
    Parse the given HTML and returns token objects (words with attached tags).

    This parses only the content of a page; anything in the head is
    ignored, and the <head> and <body> elements are themselves
    optional.  The content is then parsed by lxml, which ensures the
    validity of the resulting parsed document (though lxml may make
    incorrect guesses when the markup is particular bad).

    <ins> and <del> tags are also eliminated from the document, as
    that gets confusing.

    If include_hrefs is true, then the href attribute of <a> tags is
    included as a special kind of diffable token."""
    ...

def parse_html(html, cleanup=...):
    """
    Parses an HTML fragment, returning an lxml element.  Note that the HTML will be
    wrapped in a <div> tag that was not in the original document.

    If cleanup is true, make sure there's no <head> or <body>, and get
    rid of any <ins> and <del> tags.
    """
    ...

_body_re = ...
_end_body_re = ...
_ins_del_re = ...
def cleanup_html(html): # -> str:
    """ This 'cleans' the HTML, meaning that any page structure is removed
    (only the contents of <body> are used, if there is any <body).
    Also <ins> and <del> tags are removed.  """
    ...

end_whitespace_re = ...
def split_trailing_whitespace(word): # -> tuple[Any, Any]:
    """
    This function takes a word, such as 'test\n\n' and returns ('test','\n\n')
    """
    ...

def fixup_chunks(chunks): # -> list[token | Any] | list[Any]:
    """
    This function takes a list of chunks and produces a list of tokens.
    """
    ...

empty_tags = ...
block_level_tags = ...
block_level_container_tags = ...
def flatten_el(el, include_hrefs, skip_tag=...): # -> Generator[tuple[Literal['img'], Any, LiteralString] | LiteralString | Any | tuple[Literal['href'], Any], Any, None]:
    """ Takes an lxml element el, and generates all the text chunks for
    that tag.  Each start tag is a chunk, each word is a chunk, and each
    end tag is a chunk.

    If skip_tag is true, then the outermost container tag is
    not returned (just its contents)."""
    ...

split_words_re = ...
def split_words(text): # -> list[Any]:
    """ Splits some text into words. Includes trailing whitespace
    on each word when appropriate.  """
    ...

start_whitespace_re = ...
def start_tag(el): # -> LiteralString:
    """
    The text representation of the start tag for a tag.
    """
    ...

def end_tag(el): # -> LiteralString:
    """ The text representation of an end tag for a tag.  Includes
    trailing whitespace when appropriate.  """
    ...

def is_word(tok): # -> bool:
    ...

def is_end_tag(tok):
    ...

def is_start_tag(tok): # -> bool:
    ...

def fixup_ins_del_tags(html):
    """ Given an html string, move any <ins> or <del> tags inside of any
    block-level elements, e.g. transform <ins><p>word</p></ins> to
    <p><ins>word</ins></p> """
    ...

def serialize_html_fragment(el, skip_outer=...):
    """ Serialize a single lxml element as HTML.  The serialized form
    includes the elements tail.  

    If skip_outer is true, then don't serialize the outermost tag
    """
    ...

class InsensitiveSequenceMatcher(difflib.SequenceMatcher):
    """
    Acts like SequenceMatcher, but tries not to find very small equal
    blocks amidst large spans of changes
    """
    threshold = ...
    def get_matching_blocks(self): # -> list[Match]:
        ...
    


if __name__ == '__main__':
    ...
