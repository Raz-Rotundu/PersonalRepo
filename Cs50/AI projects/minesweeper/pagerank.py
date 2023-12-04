import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


# Used for testing
# def main():

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # The list of pages this one links to
    options = corpus[page]

    out = {}

    # If no pages are linked to, randomly choose one from the corpus
    if len(options) == 0:
        v = 1 / len(corpus)
        for link in corpus:
            out[link] = v
        return out
    else:
        # We want to add the df value to the actual options + the odds that it is chosen randomly 1-df times
        initial_prob = damping_factor / len(options)
        damp_prob = (1 - damping_factor) / len(corpus)
        # Calculate probabilities of links of page
        for link in options:
            out[link] = initial_prob + damp_prob
        # Calculate probabilities of randomly hitting any other page according to df
        for l in corpus:
            if l not in list(out.keys()):
                out[l] = damp_prob
        return out


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # The dict to be returned
    out = {}

    # The intial sampling, and generating transition model
    p = random.choice(list(corpus.keys()))
    t  = transition_model(corpus, p, damping_factor)

    # Added to out
    out[p] = 1

    # n-1 to adjust for first sample
    for i in range(n-1):

        # Separate the keys and values in transition model
        options = list(t.keys())
        option_probs = list(t.values())

        # Choose a random key based on corresponding values
        p = str(random.choices(options, weights = option_probs, k = 1))

        # Add occurence to out
        if p in list(out.keys()):
            out[p] += 1
        else:
            out[p] = 1
    # Divide number or occurences by n to compute probability
    for page in list(out.keys()):
        out[page] = (out[page] / n)
    return out


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    diff = 1
    out = {}
    N = len(corpus)
    
    # The first part of the iterative formula
    first_part = (1 - damping_factor) / N

    # Set each page's rank to 1/N
    for page in corpus:
        out[page] = 1 / N
    
    # Repeat until change is less than 0.001
    while diff > 0.001:
        # Calculate the new probability for each page in corpus
        for p in corpus:
            v = first_part + calculate_sum(p, damping_factor, corpus, out)
            # Check difference, then update value
            diff = out[p] - v
            out[p] = v
    return out


def num_links(p, corpus):
    """ Calculates the number of outbound links of a given page"""
    return(len(corpus[p]))

def calculate_sum(page, damping_factor, corpus, page_ranks):
    """ Computes the sum of PR/numlinks for all outbound links of a given page, and multiplies by camping_factor"""
    
    p = corpus[page]
    total = 0
    # A set of pages which link to this one
    links_to_this = set()

    # Find out which pages links to this one
    for p in list(corpus.keys()):
        if page in corpus[p]:
            links_to_this.add(p)

    # A page with no outbound links is interpreted as having a link to every page in the corpus + itself
    if len(p) == 0:
        for i in list(corpus.keys()):
            total += page_ranks[i] / len(corpus)
    else:
        for i in links_to_this:
            total += page_ranks[i] / num_links(i, corpus)
    total = total * damping_factor
    return total
if __name__ == "__main__":
    main()
