# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################


import json, sqlite3, os.path
from tools import *


dct = """
==hr
    2 blank tiles (scoring 0 points)
    1 point: A ×11, I ×10, E ×9, O ×9, N ×6, R ×5, S ×5, T ×5, J ×4, U ×4
    2 points: K ×3, M ×3, P ×3, V ×3
    3 points: D ×3, G ×2, L ×2, Z ×2, B ×1, Č ×1
    4 points: C ×1, H ×1, LJ ×1, NJ ×1, Š ×1, Ž ×1
    5 points: Ć ×1
    8 points: F ×1
    10 points: DŽ ×1, Đ ×1
#
==cs
    2 blank tiles (scoring 0 points)
    1 point: O ×6, A ×5, E ×5, N ×5, I ×4, S ×4, T ×4, V ×4, D ×3, K ×3, L ×3, P ×3, R ×3
    2 points: C ×3, H ×3, Í ×3, M ×3, U ×3, Á ×2, J ×2, Y ×2, Z ×2
    3 points: B ×2, É ×2, Ě ×2
    4 points: Ř ×2, Š ×2, Ý ×2, Č ×1, Ů ×1, Ž ×1
    5 points: F ×1, G ×1, Ú ×1
    6 points: Ň ×1
    7 points: Ó ×1, Ť ×1
    8 points: Ď ×1
    10 points: X ×1
#
==da
    2 blank tiles (scoring 0 points)
    1 point: E ×9, A ×7, N ×6, R ×6
    2 points: D ×5, L ×5, O ×5, S ×5, T ×5
    3 points: B ×4, I ×4, K ×4, F ×3, G ×3, M ×3, U ×3, V ×3
    4 points: H ×2, J ×2, P ×2, Y ×2, Æ ×2, Ø ×2, Å ×2
    8 points: C ×2, X ×1, Z ×1
#
==nl
    2 blank tiles (scoring 0 points)
    1 point: E ×18, N ×10, A ×6, O ×6, I ×4
    2 points: D ×5, R ×5, S ×5, T ×5
    3 points: G ×3, K ×3, L ×3, M ×3, B ×2, P ×2
    4 points: U ×3, F ×2, H ×2, J ×2, V ×2, Z ×2
    5 points: C ×2, W ×2
    8 points: X ×1, Y ×1
    10 points: Q ×1
#
==eo
    2 blank tiles (scoring 0 points).
    1 point: A ×8, E ×8, I ×8, O ×8, N ×6, R ×6, S ×6, L ×4, T ×4, U ×4
    2 points: K ×4, M ×4, D ×3, J ×3, P ×3
    3 points: F ×2, G ×2, Ĝ ×2, V ×2
    4 points: B ×2, Ĉ ×2, C ×1, Ŝ ×1
    5 points: Z ×1
    8 points: H ×1, Ŭ ×1
    10 points: Ĥ ×1, Ĵ ×1
#
==et
    2 blank tiles (scoring 0 points)
    1 point: A ×10, E ×9, I ×9, S ×8, T ×7, K ×5, L ×5, O ×5, U ×5
    2 point: D ×4, M ×4, N ×4, R ×2
    3 point: G ×2, V ×2
    4 point: B ×1, H ×2, J ×2, P ×2, Õ ×2
    5 point: Ä ×2, Ü ×2
    6 point: Ö ×2
    8 point: F ×1
    10 point: Š ×1, Z ×1, Ž ×1
#
==gl
    1 point: A ×12, E ×10, O ×9, R ×8, S ×7, I ×6, L ×6, N ×6, C ×5, T ×4
    2 points: D ×3, U ×3
    3 points: M ×4, B ×2, P ×2
    4 points: G ×2, V ×1
    5 points: F ×1, H ×1, X ×1
    6 points: Z ×1
    7 points: Ñ ×1, Q ×1
    8 points: K ×1
    9 points: W ×1, Y ×1
    10 points: J ×1
#
==el
    2 blank tiles (scoring 0 points)
    1 point: Α ×12, Ο ×9, Ε ×8, Ι ×8, Τ ×8, Η ×7, Σ ×7, Ν ×6
    2 points: Ρ ×5, Κ ×4, Π ×4, Υ ×4
    3 points: Λ ×3, Μ ×3, Ω ×3
    4 points: Γ ×2, Δ ×2
    8 points: Β ×1, Φ ×1, Χ ×1
    10 points: Ζ ×1, Θ ×1, Ξ ×1, Ψ ×1
#
==ht
    2 blank tiles (scoring 0 points)
    1 point: A ×9, N ×9, E ×8, I ×6
    2 points: È ×4, K ×4, L ×4, M ×4, O ×4, OU ×4, P ×4, S ×4, T ×4, Y ×4
    3 points: D ×3
    4 points: B ×3, CH ×2, F ×2, G ×2, J ×2, Ò ×2, R ×2, V ×2, W ×2
    7 points: Z ×1
    8 points: À ×1, UI ×1
    10 points: H ×1
#
==hu
    2 blank tiles (scoring 0 points).
    1 point: A ×6, E ×6, K ×6, T ×5, Á ×4, L ×4, N ×4, R ×4, I ×3, M ×3, O ×3, S ×3
    2 points: B ×3, D ×3, G ×3, Ó ×3
    3 points: É ×3, H ×2, SZ ×2, V ×2
    4 points: F ×2, GY ×2, J ×2, Ö ×2, P ×2, U ×2, Ü ×2, Z ×2
    5 points: C ×1, Í ×1, NY ×1
    7 points: CS ×1, Ő ×1, Ú ×1, Ű ×1
    8 points: LY ×1, ZS ×1
    10 points: TY ×1
#
==is
    2 blank tiles (scoring 0 points)
    1 point: A ×11, R ×8, I ×7, N ×7, S ×7
    2 points: T ×6, U ×6, L ×5, Ð ×4, K ×4, M ×3
    3 points: E ×3, F ×3, G ×3, Á ×2, Ó ×2
    4 points: Æ ×2, H ×1, Í ×1, Ú ×1
    5 points: B ×1, D ×1, O ×1, P ×1, V ×1, Ý ×1
    6 points: J ×1, Y ×1, Ö ×1
    7 points: É ×1, Þ ×1
    10 points: X ×1
#
==id
    2 blank tiles (scoring 0 points)
    1 point: A ×19, N ×9, E ×8, I ×8, T ×5, U ×5, R ×4, O ×3, S ×3
    2 points: K ×3, M ×3
    3 points: D ×4, G ×3
    4 points: L ×3, H ×2, P ×2
    5 points: B ×4, Y ×2, F ×1, W ×1
    8 points: C ×3, V ×1
    10 points: J ×1, Z ×1
#
==ga
    2 blank tiles (scoring 0 points)
    1 point: A ×13, H ×10, I ×10, N ×7, R ×7, E ×6, S ×6
    2 points: C ×4, D ×4, L ×4, O ×4, T ×4, G ×3, U ×3
    4 points: Á ×2, F ×2, Í ×2, M ×2
    8 points: É ×1, Ó ×1, Ú ×1
    10 points: B ×1, P ×1
#
==it
    2 blank tiles (scoring 0 points)
    1 point: O ×15, A ×14, I ×12, E ×11
    2 points: C ×6, R ×6, S ×6, T ×6
    3 points: L ×5, M ×5, N ×5, U ×5
    5 points: B ×3, D ×3, F ×3, P ×3, V ×3
    8 points: G ×2, H ×2, Z ×2
    10 points: Q ×1
#
==hira
    2 blank tiles (scoring 0 points)
    1 point: い ×4, う ×4, か ×4, し ×4, た ×4, て ×4, と ×4, の ×4, ん ×4
    2 points: き ×3, く ×3, こ ×3, つ ×3, な ×3, に ×3, は ×3, よ ×3, れ × 3
    3 points: あ ×2, け ×2, す ×2, せ ×2, も ×2, り ×2, る ×2, わ ×2, ら ×1
    4 points: さ ×1, そ ×1, ち ×1, ま ×1
    5 points: お ×1, ひ ×1, ふ ×1, ゆ ×1
    6 points: ほ ×1, め ×1, や ×1
    8 points: え ×1, へ ×1, み ×1
    10 points: ね ×1, む ×1, ろ ×1
    12 points: ぬ ×1
#
==romaji
    2 blank tiles (scoring 0 points)
    1 point: A ×12, U ×12, I ×11, O ×10, N ×7
    2 points: K ×6, S ×6, E ×5, H ×4, R ×4, T ×4
    3 points: M ×3, - ×2
    4 points: G ×2, Y ×2
    5 points: B ×2, D ×2
    6 points: J ×1, Z ×1
    8 points: F ×1, P ×1, W ×1
    10 points: C ×1
#
==la
    2 blank tiles (scoring 0 points)
    1 point: E ×12, A ×9, I ×9, V ×9, S ×8, T ×8, R ×7, O ×5
    2 points: C ×4, M ×4, N ×4, D ×3, L ×3
    3 points: Q ×3
    4 points: B ×2, G ×2, P ×2, X ×2
    8 points: F ×1, H ×1
#
==lv
    2 blank tiles (scoring 0 points)
    1 point: A ×11, I ×9, S ×8, E ×6, T ×6, R ×5, U ×5
    2 points: Ā ×4, K ×4, M ×4, N ×4, L ×3, P ×3
    3 points: D ×3, O ×3, V ×3, Z ×2
    4 points: Ē ×2, Ī ×2, J ×2
    5 points: B ×1, C ×1, G ×1
    6 points: Ņ ×1, Š ×1, Ū ×1
    8 points: Ļ ×1, Ž ×1
    10 points: Č ×1, F ×1, Ģ ×1, H ×1, Ķ ×1
#
==lt
    2 blank tiles (scoring 0 points)
    1 point: I ×11, A ×9, R ×9, E ×6, L ×6, S ×6, O ×5, T ×5, U ×5, N ×4, Ą ×1
    2 points: K ×4, D ×3, M ×3, P ×3, B ×2, G ×2, Ę ×1
    3 points: Ė ×2, Š ×2, Ų ×1
    4 points: J ×2, Į ×1, V ×1, Ž ×1
    5 points: Ū ×1, Z ×1
    6 points: Y ×1
    7 points: C ×1, Č ×1
    10 points: F ×1, H ×1
#
==mg
    2 blank tiles (scoring 0 points)
    1 point: A ×20, O ×14, N ×13, I ×11, T ×6, K ×5, E ×4, S ×4, Y ×4
    2 points: F ×2, M ×2, V ×2
    3 points: D ×2, L ×2
    4 points: B ×2, P ×2
    6 points: H ×1, J ×1, R ×1, Z ×1
    10 points: G ×1
#
==math
    3 blank tiles (scoring 0 points)
    1 point: = ×20, 0 ×7, 1 ×7, 2 ×7
    2 points: 3 ×6, 4 ×6, 5 ×6
    3 points: 6 ×5, 7 ×5, 8 ×5, + ×4, − ×4
    4 points: 9 ×4, a ×4, ÷ ×4
    10 points: ^ ×3, √ ×3
#
==no
    2 blank tiles (scoring 0 points)
    1 point: E ×9, A ×7, N ×6, R ×6, S ×6, T ×6, D ×5, I ×5, L ×5
    2 points: F ×4, G ×4, K ×4, O ×4, M ×3
    3 points: H ×3
    4 points: B ×3, U ×3, V ×3, J ×2, P ×2, Å ×2
    5 points: Ø ×2
    6 points: Y ×1, Æ ×1
    8 points: W ×1
    10 points: C ×1
#
==pl
    2 blank tiles (scoring 0 points)
    1 point: A ×9, I ×8, E ×7, O ×6, N ×5, Z ×5, R ×4, S ×4, W ×4
    2 points: Y ×4, C ×3, D ×3, K ×3, L ×3, M ×3, P ×3, T ×3
    3 points: B ×2, G ×2, H ×2, J ×2, Ł ×2, U ×2
    5 points: Ą ×1, Ę ×1, F ×1, Ó ×1, Ś ×1, Ż ×1
    6 points: Ć ×1
    7 points: Ń ×1
    9 points: Ź ×1
#
==pt
    3 blank tiles (scoring 0 points)
    1 point: A ×14, E ×11, I ×10, O ×10, S ×8, U ×7, M ×6, R ×6, T ×5
    2 points: D ×5, L ×5, C ×4, P ×4
    3 points: N ×4, B ×3, Ç ×2
    4 points: F ×2, G ×2, H ×2, V ×2
    5 points: J ×2
    6 points: Q ×1
    8 points: X ×1, Z ×1
#
==ro
    2 blank tiles (scoring 0 points)
    1 point: I ×11, A ×10, E ×9, T ×7, N ×6, R ×6, S ×6, C ×5, L ×5, U ×5
    2 points: O ×5, P ×4
    3 points: D ×4
    4 points: M ×3, F ×2, V ×2
    5 points: B ×2
    6 points: G ×2
    8 points: H ×1, Z ×1
    10 points: J ×1, X ×1
#
==sk
    2 blank tiles (scoring 0 points)
    1 point: O × 10, A × 9, E × 8, I × 6, N × 5, S × 5, V × 5, T × 4
    2 points: R × 5, K × 4, L × 4, D × 3, M × 3, P × 3, U × 3, Á × 2, B × 2, J × 2, Y × 2, Z × 2
    3 points: C × 1, Č × 1, É × 1, H × 1, Í × 1, Š × 1, Ú × 1, Ý × 1, Ž × 1
    4 points: Ť × 1
    5 points: Ľ × 1
    6 points: F × 1, G × 1
    7 points: Ň × 1, Ô × 1
    8 points: Ä × 1, Ď × 1, Ó × 1
    9 points: Ĺ × 1, Ŕ × 1, X × 1
    10 points: Q × 1, W × 1
#
==sl
    2 blank tiles (scoring 0 points)
    1 point: E ×11, A ×10, I ×9, O ×8, N ×7, R ×6, S ×6, J ×4, L ×4, T ×4
    2 points: D ×4, V ×4
    3 points: K ×3, M ×2, P ×2, U ×2
    4 points: B ×2, G ×2, Z ×2
    5 points: Č ×1, H ×1
    6 points: Š ×1
    8 points: C ×1
    10 points: F ×1, Ž ×1
#
==sv
    2 blank tiles (scoring 0 points)
    1 point: A ×8, R ×8, S ×8, T ×8, E ×7, N ×6, D ×5, I ×5, L ×5
    2 points: O ×5, G ×3, K ×3, M ×3, H ×2
    3 points: F ×2, V ×2, Ä ×2
    4 points: U ×3, B ×2, P ×2, Ö ×2, Å ×2
    7 points: J ×1, Y ×1
    8 points: C ×1, X ×1
    10 points: Z ×1
#
==tn
    2 blank tiles (scoring 0 points)
    1 point: A ×16, E ×12, O ×11, L ×9, G ×6, N ×6, T ×6, S ×5
    2 points: I ×5
    3 points: K ×4, M ×4
    4 points: B ×3
    5 points: H ×3, R ×3, D ×2, W ×2
    8 points: F ×1, P ×1, U ×1, Y ×1
    10 points: J ×1
#
==tr
    2 blank tiles (scoring 0 points)
    1 point: A ×12, E ×8, İ ×7, K ×7, L ×7, R ×6, N ×5, T ×5
    2 points: I ×4, M ×4, O ×3, S ×3, U ×3
    3 points: B ×2, D ×2, Ü ×2, Y ×2
    4 points: C ×2, Ç ×2, Ş ×2, Z ×2
    5 points: G ×1, H ×1, P ×1
    7 points: F ×1, Ö ×1, V ×1
    8 points: Ğ ×1
    10 points: J ×1 
#
==uk                             
    2 blank tiles (scoring 0 points)
    1 point: О ×10, А ×8, И ×7, Н ×7, В ×4, Е ×5, І ×5, Т ×5, Р ×5
    2 points: К ×4, С ×4, Д ×3, Л ×3, М ×4, П ×3
    3 points: У ×3
    4 points: З ×2, Я ×2, Б ×2, Г ×2
    5 points: Ч ×1, Х ×1, Й ×1, Ь ×1
    6 points: Ж ×1, Ї ×1, Ц ×1, Ш ×1
    7 points: Ю ×1
    8 points: Є ×1, Ф ×1, Щ ×1
    10 points: Ґ ×1, ' ×1
#
==cy
    2 blank tiles (scoring 0 points)
    1 point: A ×10, E ×8, N ×8, I ×7, R ×7, Y ×7, D ×6, O ×6, W ×5, DD ×4
    2 points: F ×3, G ×3, L ×3, U ×3
    3 points: S ×3, B ×2, M ×2, T ×2
    4 points: C ×2, FF ×2, H ×2, TH ×2
    5 points: CH ×1, LL ×1, P ×1
    8 points: J ×1
    10 points: NG ×1, RH ×1
#
==bopo
    2 blank tiles (scoring 0 points)
    1 point: ㄧ ×13, ㄨ ×10
    4 points: ㄉ ×8, ㄜ ×5, ㄢ ×5, ㄥ ×5
    5 points: ㄐ ×4, ㄚ×4, ㄠ ×4, ㄣ ×3
    6 points: ㄊ ×3, ㄌ ×3, ㄏ ×3, ㄕ ×3, ㄅ ×2, ㄒ×2, ㄓ ×2, ㄩ ×2, ㄟ ×2, ㄤ ×2
    7 points: ㄍ ×2, ㄛ×2, ㄡ ×2, ㄞ ×1
    8 points: ㄇ ×1, ㄋ ×1, ㄑ×1, ㄖ ×1, ㄗ  ×1, ㄝ ×1
#
==ms
    2 blank tiles (scoring 0 points)
    1 point : A ×19, N ×8, E ×7, I ×7, K ×6, U ×6, M ×5, R ×5, T ×5
    2 points : L ×4, S ×4
    3 points : G ×4, B ×3, D ×3
    4 points : H ×2, O ×2, P ×2
    5 points : J ×1, Y ×1
    8 points : C ×1, W ×1
    10 points : F ×1, Z ×1
"""


for l in dct.split('#'):
    my_letters = {}
    my_cx= {}
    cx = 1
    for a in l.split('\n'):
        if a.strip() == '':continue
        if '==' in a: l_code = a.strip().replace('==', '')
        elif 'blank' in a: my_letters['*'] = (int(a.strip()[0]), 0)
        else:
            a1,a2 = a.split(':')
            v = int(a1.strip().split(' ')[0])
            for b in a2.split(','):
                b1,b2 = b.split('×')
                l = b1.strip()
                n = int(b2.strip())
                if len(l) == 1:
                    my_letters[l] = (n, v)
                else:
                    my_letters[str(cx)] = (n, v)
                    my_cx[str(cx)] = l
                    cx += 1
    
    print("'"+l_code+"':", my_cx,',')
    print("'"+l_code+"':", my_letters,',')

