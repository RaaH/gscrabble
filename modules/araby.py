# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################


#aالحروف------------------------------------------------------------------------

HAMZA            = '\u0621'
ALEF_MADDA       = '\u0622'
ALEF_HAMZA_ABOVE = '\u0623'
WAW_HAMZA        = '\u0624'
ALEF_HAMZA_BELOW = '\u0625'
YEH_HAMZA        = '\u0626'
ALEF             = '\u0627'
BEH              = '\u0628'
TEH_MARBUTA      = '\u0629'
TEH              = '\u062a'
THEH             = '\u062b'
JEEM             = '\u062c'
HAH              = '\u062d'
KHAH             = '\u062e'
DAL              = '\u062f'
THAL             = '\u0630'
REH              = '\u0631'
ZAIN             = '\u0632'
SEEN             = '\u0633'
SHEEN            = '\u0634'
SAD              = '\u0635'
DAD              = '\u0636'
TAH              = '\u0637'
ZAH              = '\u0638'
AIN              = '\u0639'
GHAIN            = '\u063a'
FEH              = '\u0641'
QAF              = '\u0642'
KAF              = '\u0643'
LAM              = '\u0644'
MEEM             = '\u0645'
NOON             = '\u0646'
HEH              = '\u0647'
WAW              = '\u0648'
ALEF_MAKSURA     = '\u0649'
YEH              = '\u064a'



################################################################################
#========================== TETRIS =============================================
################################################################################

elletters = [
    HAMZA,ALEF_MADDA,ALEF_HAMZA_ABOVE,WAW_HAMZA,ALEF_HAMZA_BELOW,
    YEH_HAMZA,ALEF,BEH,TEH_MARBUTA,TEH,THEH,JEEM,HAH,KHAH,DAL,THAL,
    REH,ZAIN,SEEN,SHEEN,SAD,DAD,TAH,ZAH,AIN,GHAIN,FEH,QAF,
    KAF,LAM,MEEM,NOON,HEH,WAW,ALEF_MAKSURA,YEH
    ]


################################################################################
#========================== SCRABBLE ===========================================
################################################################################



arbic_letters = {
    "*": (2,0), 
    ALEF:(8,1), LAM:(4,1), MEEM:(3,1), WAW:(3,1), YEH:(3,1), NOON:(3,1), HEH:(3,1), 
    JEEM:(4,1), ALEF_MAKSURA:(2,1), TEH_MARBUTA:(2,1), KHAH:(3,1), HAH:(3,1), 
    REH:(3,2), BEH:(4,2), TEH:(4,2), THEH:(3,2), DAL:(3,2), SEEN:(3,2), 
    FEH:(3,3), SHEEN:(3,3), THAL:(3,3), ZAIN:(3,3), 
    QAF:(3,4), AIN:(3,4), KAF:(3,4), SAD:(3,4), DAD:(3,4), TAH:(2,4), 
    ZAH:(2,5), 
    YEH_HAMZA:(1,6), 
    GHAIN:(2,8), HAMZA:(1,8), ALEF_MADDA:(1,8), 
    WAW_HAMZA:(1,10), ALEF_HAMZA_BELOW:(1,10), ALEF_HAMZA_ABOVE:(1,10)
    }

arbic_test = {
    "*": (2,0), 
    ALEF:(2,1), LAM:(1,1), MEEM:(1,1), WAW:(1,1), YEH:(1,1), NOON:(1,1), HEH:(1,1), 
    JEEM:(1,1), ALEF_MAKSURA:(1,1), TEH_MARBUTA:(1,1), KHAH:(1,1), HAH:(1,1), 
    REH:(1,2), BEH:(1,2), TEH:(1,2), THEH:(1,2), DAL:(1,2), SEEN:(1,2), 
    FEH:(1,3), SHEEN:(1,3), THAL:(1,3), ZAIN:(1,3), 
    QAF:(1,4), AIN:(1,4), KAF:(1,4), SAD:(1,4), DAD:(1,4), TAH:(1,4), 
    ZAH:(1,5), GHAIN:(1,8)
    }

