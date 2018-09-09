#!/usr/bin/env python
# Re: macro expansion methods testing
# - jiw -  8 Sept 2018
from re import sub, search

# Macros: Let x represent a macro name formed of letters, digits, or
# underscore in any order or length.  In the macro system implemented
# here, if x is a defined macro and s is a string to be processed, the
# text of x is substituted into s where-ever @x% appears in s.

# The macro system supports several other operations besides @x% text
# substitution.  In text to be processed, operations are specified in
# the form @xk where x is a macro name and k is a special character
# from the set { %, ^, #, +, -, !, =, ? }.  Some other characters (eg,
# {., |, $, :, ;, *, ~, & }) might be used in future. Briefly, the
# supported operations are as follows:

# Form   Purpose
#  @x%   Substitute text of macro x
#  @x#   Substitute value of counter x
#  @x^   Substitute value of counter x and add 1 to counter x
#  @x+   Substitute '' and add 1 to counter x
#  @x-   Substitute '' and subtract 1 from counter x
#  @x?   Substitute '' and undefine macro x and its counter
#  @x=   Substitute text of macro x if counter x is zero, else ''
#  @x!   Substitute text of macro x if counter x is non-zero, else ''

# Strings are processed left to right during macro expansion, with
# processing continuing until no more operations remain to do.

# With one exception (the @x? form), an input form @xk passes to
# output unchanged if x is not defined.  Example: if macro b is not
# defined, processing input 'a@b%c' results in 'a@b%c' output.

# However, @x? gets squeezed out, without regard to whether x is
# defined.  Examples: Processing input 'a@b?c@b%d' results in 'ac@b%d'
# output and b undefined; processing input 'Row @c@b?^' results in
# output 'Row @c^' and b undefined.  (The left-to-right input
# processing in use does not move back to recognize that an expandable
# '@c^' got created.)

# Note, each macro has an associated counter that is zeroed whenever
# the macro is defined and increases when used via `@x^` within a
# macro definition string), or does not increase when used via `@x#`.
# For example, if m='a@#b@#c@#d', processing 'e@m%f g@m%h' produces
# 'ea0b1c2df ga3b4c5dh'.

# Macro expansions can be nested; for example, <macro a='m@c%n@b%o'
# b='@d%' c='f@d%g' d='5'/> <elt id='p@a%q'/> first expands 'p@a%q' to
# 'pm@c%n@b%oq', then successively to 'pmf@d%gn@b%oq', 'pmf5gn@b%oq',
# 'pmf5gn@d%oq', and 'pmf5gn5oq'.  Note, processing is left to right;
# portions of the input left of an operation point become inactive.

# This program defines seven simple text substitution macros, called
# a, b, c, d, m, hh, kk, and tt, that can be used to test substitution
# syntax and behavior.  A default string,
# 'aa@bb%gg@hh%tt@kk%cc@tt%dd@bb%ee' also is provided, or the user can
# provide a string as command line input.

# Macros for the boxgrid program are defined within <macro ... /> lines
# in an XML file.  Macro substitution in boxgrid occurs when @x%
# appears in a right-hand-side text string.

# In boxgrid usage, macros can be defined or redefined when needed.
# For example, if you want to define elements rowwise, you could write
# <macro c='@#'/> before each row's series of elements, and within each
# <elt> line, write col='@c'.

def macroSubst(tin, recot, recon):
    lup=0
    LH = ''
    RH = tin
    while True:                 # Expand macro texts
        lup+=1
        if lup>200: return '(macroSubst exceeded {} passes & gave up)'.format(lup)
        # RE gets four items: head part; macro name; macro opcode; tail part.
        s = search(r'(.*?)@(\w+)([-%^#+!=?])(.*)', RH)
        if s:
            headpt = s.expand(r'\1')
            mname  = s.expand(r'\2')
            opcode = s.expand(r'\3')
            tailpt = s.expand(r'\4')
            #print 'LHRH:  {}   s1:{},  s2:{},  s3:{},  s4:{},  LH:{},  RH:{}'.format(LH+RH, headpt, mname, opcode, tailpt, LH, RH)
            if opcode=='?':
                LH = LH + headpt
                RH = tailpt
                recot.pop(mname, None) # Undefine specified macro
                recon.pop(mname, None)
            elif mname in recot:
                mBody = recot[mname]
                mCounter = recon[mname]
                if opcode=='#' or opcode=='^':
                    mBody = str(mCounter)
                elif opcode=='+' or opcode=='-' or (opcode=='=' and mCounter != 0) or (opcode=='!' and mCounter == 0):
                    mBody = ''
                if opcode=='^' or opcode=='+':
                    recon[mname] += 1 # Increase counter
                elif opcode=='-':
                    recon[mname] -= 1 # Decrease counter  
                # Put expanded macro text into RH
                LH = LH + headpt
                RH = mBody + tailpt
            else:
                LH = LH + s.expand(r'\1@')
                RH = s.expand(r'\2\3\4') 
        else:
            break
    return LH+RH

# Set up to test if recot as shown first expands 'p@a%q' to
#   'pm@c%n@b%oq', then successively to 'pmf@d%gn@b%oq',
#   'pmf5gn@b%oq', 'pmf5gn@d%oq', and 'pmf5gn5oq'.
if __name__ == '__main__':
    import sys
    recot = { 'a':'m@c%n@b%o', 'b':'@d%', 'c':'f@d%g', 'd':'5',
              'm':'a@m^b@m^c@m^d', 'hh': 'uuH@hh^vv', 'kk': 'yyKzz', 'tt':
              'rr@kk%ss@rr^tt'}
    recon = {'a':31, 'b':42, 'c':53, 'd':64, 'm':0, 'hh': 3, 'kk': 7, 'tt': 23 }

    print ('recot: {}'.format(recot))
    print ('recon: {}'.format(recon))      
    rin = sys.argv[1] if len(sys.argv) > 1  else 'aa@bb%gg@hh%tt@kk%cc@tt%dd@bb%ee'
    print ('rin:   {}'.format(rin))
    rot = macroSubst(rin, recot, recon)
    print ('rot:   {}'.format(rot))
    print ('recon: {}'.format(recon))
    print ('recot: {}'.format(recot))
