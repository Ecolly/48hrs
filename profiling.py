import pstats
from pstats import SortKey

p = pstats.Stats("profile.out")
p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(20)



#python -m cProfile -o profile.out your_script.py