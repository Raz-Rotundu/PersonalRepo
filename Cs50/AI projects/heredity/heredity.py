import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    people_prob = {}

    for person in people:
        # Determining the what we want to find out about the person(trait, gene etc)
        status = 0
        trait = "f"
        parents = people[person]
        if person in one_gene:
            status  = 1
        elif person in two_genes:
            status = 2

        if person in have_trait:
            trait = "t"

        # Calculate gene and trait probabilities of the person if NO PARENTS
        if parents['mother'] == None and parents['father'] == None:
            if status  == 0:
                g = PROBS["gene"][0]
                if trait == "t":
                    t = PROBS["trait"][0][True]
                elif trait == "f":
                    t = PROBS["trait"][0][False]
            elif status == 1:
                g = PROBS["gene"][1]
                if trait == "t" :
                    t = PROBS["trait"][1][True]
                elif trait == "f":
                    t = PROBS["trait"][1][False]
            elif status == 2:
                g = PROBS["gene"][2]
                if trait == "t" :
                    t = PROBS["trait"][2][True]
                elif trait == "f":
                    t = PROBS["trait"][2][False]

            # Update the dictionary to show the probability of this person with the correct traits
            people_prob[person] = g * t

        # If the person HAS PARENTS
        else:
            if status == 0:
                # Get parents
                par1 = parents['mother']
                par2 = parents['father']

                # Check how many of the genes does parent 1 have, and its probability of passing it on
                if par1 in one_gene:
                    p1 = 0.5
                # Odds of passing it on are 1 - mutation rate when 2 alleles
                elif par1 in two_genes:
                    p1 = 1 - PROBS["mutation"]
                # Odds of passing it on are 0 + mutation rate when 0 alleles
                else:
                    #p1 = 1 - PROBS["mutation"]
                    p1 = 0 + PROBS["mutation"]

                    # Now repeat for parent 2
                if par2 in one_gene:
                    p2 = 0.5
                elif par2 in two_genes:
                    p2 = 1 - PROBS["mutation"]
                else:
                    p2 = 0 + PROBS["mutation"]

                # Odds of getting zero is odds of not inheriting from both mother and father
                g = (1 - p1) * (1 - p2)

                # Calculate probability of manifesting a trait
                if trait == "f":
                    t = PROBS["trait"][0][False]
                elif trait == "t":
                    t = PROBS["trait"][0][True]

                # Update dictionary with this probability
                people_prob[person] = (t * g)

            elif status == 1:
                # Get the parents
                par1 = parents['mother']
                par2 = parents['father']

                # Check how many of the genes does parent 1 have, and its probability of passing it on
                if par1 in one_gene:
                    p1 = 0.5
                elif par1 in two_genes:
                    p1 = 1 - PROBS["mutation"]
                else:
                    p1 = 0 + PROBS["mutation"]

                # Now repeat for parent 2
                if par2 in one_gene:
                    p2 = 0.5
                elif par2 in two_genes:
                    p2 = 1 - PROBS["mutation"]
                else:
                    p2 = 0 + PROBS["mutation"]

                # Odds of inheriting from one means either got it from p1 and not p2, or p2 and not p1
                g = ((1 - p1) * p2) + ((1 - p2) * p1)

                # Calculate probability of manifesting a trait
                if trait == "f":
                        t = PROBS["trait"][1][False]

                elif trait == "t":
                        t = PROBS["trait"][1][True]

                # Update dictionary with this probability
                people_prob[person] = (t * g)
            elif status == 2:
                # Get the parents
                par1 = parents['mother']
                par2 = parents['father']

                # Check how many of the genes does parent 1 have, and its probability of passing it on
                if par1 in one_gene:
                    p1 = 0.5
                elif par1 in two_genes:
                    p1 = 1 - PROBS["mutation"]
                else:
                    p1 = 0 + PROBS["mutation"]

                # Now repeat for parent 2
                if par2 in one_gene:
                    p2 = 0.5
                elif par2 in two_genes:
                    p2 = 1 - PROBS["mutation"]
                else:
                    p2 = 0 + PROBS["mutation"]

                # Odds you inherited from mom and inherited from dad
                g = (p1 * p2)

                # Calculate probability of manifesting a trait
                if trait == "f":
                    t = PROBS["trait"][2][False]
                elif trait ==  "t":
                    t = PROBS["trait"][2][True]

                # Update dictionary with this probability
                people_prob[person] = (t * g)

    # Compute the final joint probability
    values = list(people_prob.values())
    total = 1
    for i in range(len(values)):
        total = total * values[i]

    # Return value
    return total


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # Will be used to indicate if the person is in onegene, twogenes or havetrait categories
        status = None
        trait = None

        # Checking if the person is in the three categories
        if person in one_gene:
            status = 1
        elif person in two_genes:
            status = 2
        else:
            status = 0

        if person in have_trait:
            trait  = True
        else:
            trait = False

        # Updating the P value acording to which categories the person is in
        probabilities[person]["gene"][status] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
     # x / sum of all numbers
    for person in probabilities:
         # d is the dictionary containing probability distribution for this person's gene
         d = probabilities[person]["gene"]
         # The actual probabilities to be found in d
         vals = list(d.values())
         total = sum(vals)
         # Updating each one according to formula
         for i in d:
             d[i] = d[i] / total

         # Normalize trait probabilities
         d = probabilities[person]["trait"]
         vals = list(d.values())
         total = sum(vals)
         # Updating each one according to formula
         for j in d:
            if total != 0:
                d[j] = d[j] / total
            else:
                d[j] = 0


if __name__ == "__main__":
    main()
