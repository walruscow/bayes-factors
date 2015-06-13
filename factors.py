from collections import defaultdict

class Factor():
    def __init__(self, vars, probabilities):
        """ Initialize a Factor with some set of variables and their
        corresponding probabilities. """
        self.vars = tuple(vars)
        self.probabilities = tuple(probabilities)


    def __str__(self):
        """ A vertical list of the whole factor. """
        # Left column may have up to 1 ~ added for each var
        leftWidth = len(self.vars) + sum(len(v) for v in self.vars)
        # This is max length for {:3g}
        rightWidth = 8
        lines = []

        for vals, prob in self.probabilities:
            varString = ''
            # Mark false with a tilde
            for idx, v in enumerate(self.vars):
                varString += v if vals[idx] else '~' + v
            # Three decimals
            probStr = '{:3g}'.format(prob).ljust(rightWidth)
            lines.append('{} {}'.format(varString.ljust(leftWidth), probStr))
        return '\n'.join(lines)


    def _getVals(self, vars, tpl):
        ret = []
        vars = set(vars)
        for i, v in enumerate(self.vars):
            if v in vars:
                ret.append(tpl[i])
        return tuple(ret)


    def __mul__(self, other):
        """ Multiply two factors. """
        # All the common variables (as strings) (in order)
        s1 = set(self.vars)
        s2 = set(other.vars)
        commonVars = list(s1 & s2)
        sVars = list(s1 - s2)
        oVars = list(s2 - s1)

        def makeCommonIndexes(factor, commonVars):
            return [factor.vars.index(v) for v in commonVars]

        # Indexes in same order as "commonVars" mapping to indexes in factor
        commonIndexes1 = makeCommonIndexes(self, commonVars)
        commonIndexes2 = makeCommonIndexes(other, commonVars)

        newProbs = []
        for sVals, sProb in self.probabilities:
            # Common values
            sCommonVals = self._getVals(commonVars, sVals)
            for oVals, oProb in other.probabilities:
                oCommonVals = other._getVals(commonVars, oVals)
                if sCommonVals == oCommonVals:
                    # Has all common values the same: New entry
                    sVals = self._getVals(sVars, sVals)
                    oVals = other._getVals(oVars, oVals)
                    # We will put our unique values, then the common ones, then
                    # the ones unique to the other factor
                    newVals = sVals + sCommonVals + oVals
                    newProbs.append((newVals, sProb * oProb))

        return Factor(sVars + commonVars + oVars, newProbs)


    def restrict(self, variable, value):
        """ Restrict a variable to a given value. """
        if variable not in self.vars:
            raise ValueError('Given variable {} not in factor'.format(variable))

        index = self.vars.index(variable)
        newVars = tuple(v for v in self.vars if v != variable)
        newProbs = []

        for vals, prob in self.probabilities:
            # Keep only entries with the correct value for the variable
            if vals[index] != value: continue
            # Remove the value at the index of our variable to restrict
            newVals = (vals[i] for i, v in enumerate(self.vars) if i != index)
            newVals = tuple(newVals)
            newProbs.append((newVals, prob))

        # Immutability 4eva
        return Factor(newVars, newProbs)


    def sumout(self, var):
        """ Sum out a given variable. """
        if var not in self.vars:
            raise ValueError('Given variable {} not in factor'.format(var))

        newVars = [v for v in self.vars if v != var]
        # Use a dictionary to collect like items (without given var)
        newProbs = defaultdict(int)
        for vals, prob in self.probabilities:
            newProbs[self._getVals(newVars, vals)] += prob

        newProbs = tuple(i for i in newProbs.items())
        return Factor(newVars, newProbs)


    def normalize(self):
        """ Normalize probabilities. """
        pass


def multiply(f1, f2):
    return f1 * f2


def restrict(factor, var, val):
    return factor.restrict(var, val)


def sumout(factor, var):
    return factor.sumout(var)


def normalize(factor):
    return factor.normalize()


def inference(factorList, queryVars, hiddenVars, evidence):
    """ Compute P(queryVars | evidence) by variable elimination.  This first
    restricts the factors according to the evidence, then sums out the hidden
    variables, in order.
    Finally, the result is normalized to return a probability over a
    distribution that sums to 1.
    """
    pass


if __name__ == '__main__':
    ab = Factor('ab',
                (((True, True), 0.9),
                 ((True, False), 0.1),
                 ((False, True), 0.4),
                 ((False, False), 0.6)))
    #bc = Factor('bc',
    #            (((True, True), 0.7),
    #             ((True, False), 0.3),
    #             ((False, True), 0.8),
    #             ((False, False), 0.2)))
    #print(ab * bc)
    #
    #
    #a = Factor('a', (((True,), 0.4), ((False,), 0.6)))
    #print('a\n{}'.format(a))
    #b = Factor('b', (((True,), 0.2), ((False,), 0.8)))
    #print('b\n{}'.format(b))
    #print('-'*30)
    #print('a * b')
    #print(a * b)
    #print('-'*30)
    print('ab\n{}\n{}'.format('-'*20,ab))
    print('-'*20)
    print('ab.sumout(a)')
    print('-'*20)
    print(ab.sumout('a'))
