s1 = "I love mis"
s2 = "I love danyboi!!!"

def is_permutation(s1, s2): 


  s1 = s1.replace(" ", "")
  s2 = s2.replace(" ", "")
  print s1, s2

  s1 = ''.join(sorted(s1))
  s2 = ''.join(sorted(s2))
  print s1, s2

  s1 = s1.lower()
  s2 = s2.lower()
  print s1, s2


  if len(s1) == len(s2):
    if s1 == s2:
      return True
      print "Yes"
    else:
        return False
        print "No"
  else:
    return False
    print "NO"

is_permutation(s1, s2)