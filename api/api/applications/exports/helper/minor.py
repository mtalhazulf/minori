import base64
from datetime import datetime

from fpdf import FPDF, HTMLMixin

from api.font import (
    FONT_DEJAVU_SANS_CONDENSED,
    FONT_DEJAVU_SANS_CONDENSED_BOLD,
    FONT_DEJAVU_SANS_CONDENSED_BOLD_OBLIQUE,
    FONT_DEJAVU_SANS_CONDENSED_OBLIQUE,
    FONT_DEJAVU_SANS_MONO,
    FONT_DEJAVU_SANS_MONO_BOLD,
    FONT_DEJAVU_SANS_MONO_BOLD_OBLIQUE,
    FONT_DEJAVU_SANS_MONO_OBLIQUE,
)


def split_sentence(max_length, sentence):
    if len(sentence) > max_length:
        last_space_index = sentence[:max_length].rfind(" ")
        if last_space_index != -1:
            txt = sentence[:last_space_index]
            rest_of_string = sentence[last_space_index + 1 :]
        else:
            txt = sentence[:max_length]
            rest_of_string = sentence[max_length:]
    else:
        txt = sentence
        rest_of_string = ""
    return txt, rest_of_string


class PDF(FPDF, HTMLMixin):
    def create_section_2page(self):
        # Sezione 1
        self.cell(
            0,
            h=5,
            txt=" ",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.cell(
            0,
            h=5,
            txt=" ",
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.set_font(size=8)
        self.set_y(10.5)
        self.set_x(104)
        self.set_font("DejaVu", "B")
        self.cell(
            5,
            h=5,
            txt=" ",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_font(size=10)
        self.set_font("DejaVu", "B")
        self.cell(0, h=5, txt="Sezione aggiuntiva percorso evolutivo  ", border=0, ln=1, align="", fill=False, link="")
        self.set_font("DejaVu")
        self.set_font(size=10.5)
        self.rect(11, 20, 187, 100, style="")

    def create_section_1(self):
        # Sezione 1
        self.cell(
            0,
            h=5,
            txt="Alla Sezione Istituti-Procura della Repubblica presso il Tribunale per i Minorenni",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.cell(
            0,
            h=5,
            txt="Viale Colli Aminei 42 80131 Napoli tel.7447540/42-",
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.set_font(size=8)
        self.set_y(10.5)
        self.set_x(102)
        self.set_font("DejaVu", "B")
        self.cell(
            5,
            h=5,
            txt=" istituti.procmin.napoli@giustizia.it",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_font(size=10)
        self.set_font("DejaVu", "B")
        self.cell(0, h=5, txt="Prot.667/05  ", border=0, ln=1, align="", fill=False, link="")
        self.set_font("DejaVu")
        self.set_font(size=10.5)
        self.rect(11, 20, 140, 23, style="")
        self.line(34, 28, 148, 28)
        self.ln()
        self.line(34, 34, 100, 34)
        self.ln()
        self.line(34, 40, 100, 40)
        self.line(110, 34, 148, 34)
        self.line(110, 40, 148, 40)
        self.set_y(23)
        self.set_x(14)
        self.cell(0, h=6, txt="Comunità", border=0, ln=1, align="", fill=False, link="")
        self.cell(0, h=6, txt="Via", border=0, ln=1, align="", fill=False, link="")
        self.cell(0, h=6, txt="Comune", border=0, ln=1, align="", fill=False, link="")
        self.set_y(30)
        self.set_x(101)
        self.cell(0, h=6, txt="Tel.", border=0, ln=1, align="", fill=False, link="")
        self.set_y(36)
        self.set_x(101)
        self.cell(0, h=6, txt="Prov.", border=0, ln=1, align="", fill=False, link="")

    def add_to_section_2page(self, info):
        self.set_xy(14, 23)
        self.multi_cell(185, 6, txt=info, border=0, align="", fill=False)

    def add_to_section_1(self, community):
        self.set_y(23)
        self.set_x(33)
        self.cell(
            0,
            h=6,
            txt=checkField("name", community),
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_x(33)
        self.cell(
            0,
            h=6,
            txt=checkField("address", community),
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_x(33)
        self.cell(
            0,
            h=6,
            txt=checkField("municipality", community),
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(29)
        self.set_x(111)
        self.cell(
            0,
            h=6,
            txt=checkField("phone_number", community),
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(35)
        self.set_x(111)
        self.cell(
            0,
            h=6,
            txt=checkField("county", community),
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )

    def create_section_2(self):
        # Sezione 2
        self.rect(155, 6, 47, 23, style="")
        self.rect(155, 31, 47, 36, style="")
        self.set_font(size=6)
        self.set_y(7.5)
        self.set_x(165.2)
        self.cell(
            0,
            h=6,
            txt="RISERVATO ALL'UFFICIO",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.line(170, 17, 195, 17)
        self.line(170, 23, 195, 23)
        self.set_font(size=8)
        self.set_y(12)
        self.set_x(160)
        self.cell(0, h=6, txt="R.IST.", border=0, ln=1, align="", fill=False, link="")
        self.set_y(19)
        self.set_x(160)
        self.cell(0, h=6, txt="R.MIN.", border=0, ln=1, align="", fill=False, link="")
        self.set_font("DejaVu", size=11.5)
        self.set_y(44)
        self.set_x(174)
        self.cell(0, h=6, txt="Foto", border=0, ln=1, align="", fill=False, link="")
        self.set_y(49)
        self.set_x(169)
        self.cell(0, h=6, txt="Del minore", border=0, ln=1, align="", fill=False, link="")

    def create_section_3(self):
        # SEZIONE 3
        self.set_font("DejaVu", "B", size=12)
        self.set_y(49)
        self.set_x(38)
        self.cell(
            0,
            h=6,
            txt="SCHEDA INFORMATIVA DEL MINORE",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )

        self.set_font("DejaVu")
        self.set_font(size=9.5)
        self.set_y(56)
        self.set_x(13)
        self.cell(
            0,
            h=6,  # x+3
            txt="Cognome e Nome",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.line(48, 61, 150, 61)
        self.cell(0, h=6, txt="Nato/a il", border=0, ln=1, align="", fill=False, link="")
        self.line(31, 67, 88, 67)
        self.cell(0, h=5, txt="Residente", border=0, ln=1, align="", fill=False, link="")
        self.line(31, 72, 118, 72)
        self.cell(0, h=5, txt="Paternità:", border=0, ln=1, align="", fill=False, link="")
        self.line(31, 77, 108, 77)
        self.cell(0, h=5, txt="Maternità:", border=0, ln=1, align="", fill=False, link="")
        self.line(31, 82, 108, 82)
        self.cell(0, h=5, txt="Tutore", border=0, ln=1, align="", fill=False, link="")
        self.line(31, 87, 108, 87)
        self.cell(
            0,
            h=5,
            txt="Assistente sociale",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.line(41, 92, 95, 92)
        self.cell(0, h=5, txt="Importo Euro", border=0, ln=1, align="", fill=False, link="")
        self.line(36, 97, 67, 97)
        self.set_font("DejaVu", "B", size=8)
        self.cell(
            0,
            h=5,
            txt="Data di Ingresso",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.line(43, 102, 73, 102)
        self.set_font("DejaVu", size=9.5)
        self.cell(
            0,
            h=5,
            txt="Condizioni fisiche e psichiche del minore all'ingresso:",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.line(96, 107, 200, 107)
        self.set_y(63)
        self.set_x(90)
        self.cell(0, h=5, txt="a:", border=0, ln=1, align="", fill=False, link="")
        self.line(98, 67, 150, 67)
        self.set_y(68)
        self.set_x(120)
        self.cell(0, h=5, txt="Prov:", border=0, ln=1, align="", fill=False, link="")
        self.line(132, 72, 150, 72)
        self.set_y(73)
        self.set_x(110)
        self.cell(0, h=5, txt="Res:", border=0, ln=1, align="", fill=False, link="")
        self.line(118, 77, 200, 77)
        self.set_y(78)
        self.set_x(110)
        self.cell(0, h=5, txt="Res:", border=0, ln=1, align="", fill=False, link="")
        self.line(118, 82, 200, 82)
        self.set_y(83)
        self.set_x(110)
        self.cell(0, h=5, txt="Res:", border=0, ln=1, align="", fill=False, link="")
        self.line(118, 87, 160, 87)
        self.set_y(88)
        self.set_x(97)
        self.cell(0, h=5, txt="Comune di:", border=0, ln=1, align="", fill=False, link="")
        self.line(118, 92, 160, 92)
        self.set_y(83)
        self.set_x(162)
        self.cell(0, h=5, txt="Tel:", border=0, ln=1, align="", fill=False, link="")
        self.line(170, 87, 200, 87)
        self.set_y(88)
        self.set_x(162)
        self.cell(0, h=5, txt="Tel:", border=0, ln=1, align="", fill=False, link="")
        self.line(170, 92, 200, 92)
        self.set_y(93)
        self.set_x(68)
        self.cell(0, h=5, txt="Ente erogatore", border=0, ln=1, align="", fill=False, link="")
        self.line(93, 97, 200, 97)
        self.set_y(98)
        self.set_x(75)
        self.cell(0, h=5, txt="Motivazione:", border=0, ln=1, align="", fill=False, link="")
        self.line(96, 102, 200, 102)
        self.set_line_width(0.4)
        self.line(14, 112, 200, 112)

    def add_to_section_3(self, minor):
        self.set_y(56)
        self.set_x(48)
        self.cell(
            0,
            h=6,
            txt=minor["surname"] + " " + minor["name"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_x(33)
        # minor["birthdate"].strftime("%d/%m/%Y")
        self.cell(
            0,
            h=6,
            txt=minor["birthdate"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_x(33)
        self.cell(0, h=5, txt=minor["resident"], border=0, ln=1, align="", fill=False, link="")
        self.set_x(33)
        self.cell(
            0,
            h=5,
            txt=minor["paternity"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_x(33)
        self.cell(
            0,
            h=5,
            txt=minor["maternity"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_x(33)
        self.cell(
            0,
            h=5,
            txt=minor["legal_guardian"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_x(43)
        self.cell(
            0,
            h=5,
            txt=minor["social_worker"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_x(35)
        self.cell(
            0,
            h=5,
            txt=minor["amount_euro"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_x(41)
        self.cell(
            0,
            h=5,
            txt=minor["entry_date"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_x(95)
        txt, rest_of_string = split_sentence(67, minor["conditions"])
        self.set_font("DejaVuMono", size=8)
        self.cell(
            0,
            h=5,
            txt=txt,
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(108)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt=rest_of_string,
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVu", size=9.5)
        self.set_y(63)
        self.set_x(96)
        self.cell(
            0,
            h=5,
            txt=minor["birthplace"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(68)
        self.set_x(130)
        self.cell(0, h=5, txt=minor["county"], border=0, ln=1, align="", fill=False, link="")
        self.set_y(73)
        self.set_x(120)
        self.cell(
            0,
            h=5,
            txt=minor["paternity_residence"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(78)
        self.set_x(120)
        self.cell(
            0,
            h=5,
            txt=minor["maternity_residence"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(83)
        self.set_x(120)
        self.cell(
            0,
            h=5,
            txt=minor["legal_guardian_residence"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(88)
        self.set_x(120)
        self.cell(
            0,
            h=5,
            txt=minor["social_worker_municipality"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(83)
        self.set_x(170)
        self.cell(
            0,
            h=5,
            txt=minor["legal_guardian_phone_number"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(88)
        self.set_x(170)
        self.cell(
            0,
            h=5,
            txt=minor["social_worker_phone_number"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(93)
        self.set_x(98)
        self.cell(
            0,
            h=5,
            txt=minor["supplying_authority"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVuMono", size=8)
        self.set_y(98)
        self.set_x(95)
        self.cell(
            0,
            h=5,
            txt=minor["entry_motivation"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVu", size=9.5)

    def create_section_4(self):
        # SEZIONE 4
        self.set_line_width(0.2)
        self.line(46, 117, 73, 117)  # Data di dimissioni
        self.line(96, 117, 200, 117)  # motivazione
        self.set_y(114)
        self.set_x(13)
        self.set_font("DejaVu", "B", size=8)
        self.cell(
            0,
            h=5,
            txt="Data di dismissioni",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVu", size=9.5)
        self.set_y(114)
        self.set_x(75)
        self.cell(0, h=5, txt="Motivazione", border=0, ln=1, align="", fill=False, link="")
        self.set_font(size=7.5)
        self.set_y(119)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="Portatore di handicap:",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(44, 120, 3, 3, style="")  # fisici
        self.set_y(119)
        self.set_x(47)
        self.cell(0, h=5, txt="fisici", border=0, ln=1, align="", fill=False, link="")
        self.rect(54, 120, 3, 3, style="")  # psichici
        self.set_y(119)
        self.set_x(57)
        self.cell(0, h=5, txt="psichici", border=0, ln=1, align="", fill=False, link="")
        self.rect(68, 120, 3, 3, style="")  # si
        self.set_y(119)
        self.set_x(71)
        self.cell(0, h=5, txt="SI", border=0, ln=1, align="", fill=False, link="")
        self.rect(78, 120, 3, 3, style="")  # no
        self.set_y(119)
        self.set_x(81)
        self.cell(0, h=5, txt="NO", border=0, ln=1, align="", fill=False, link="")
        self.set_y(119)
        self.set_x(90)
        self.cell(
            0,
            h=5,
            txt="Familiari presenti in struttura:",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(128, 120, 3, 3, style="")  # SI
        self.set_y(119)
        self.set_x(131)
        self.cell(0, h=5, txt="SI  (", border=0, ln=1, align="", fill=False, link="")
        self.rect(138, 120, 3, 3, style="")  # madre
        self.set_y(119)
        self.set_x(141)
        self.cell(0, h=5, txt="Madre", border=0, ln=1, align="", fill=False, link="")
        self.rect(151, 120, 3, 3, style="")  # fratello/i
        self.set_y(119)
        self.set_x(154)
        self.cell(0, h=5, txt="fratello/i", border=0, ln=1, align="", fill=False, link="")
        self.rect(167, 120, 3, 3, style="")  # sorella/e
        self.set_y(119)
        self.set_x(170)
        self.cell(0, h=5, txt="sorella/e ) -", border=0, ln=1, align="", fill=False, link="")
        self.rect(188, 120, 3, 3, style="")  # no
        self.set_y(119)
        self.set_x(191)
        self.cell(0, h=5, txt="NO", border=0, ln=1, align="", fill=False, link="")
        self.set_font("DejaVu", "B", size=9)
        self.set_y(127)
        self.set_x(13)
        self.cell(0, h=5, txt="Proveniente da:", border=0, ln=1, align="", fill=False, link="")
        self.set_y(127)
        self.set_x(88)
        self.cell(
            0,
            h=5,
            txt="Collocati su disposizione di:",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVu")
        self.rect(13, 134, 3, 3, style="")  # Famiglia di origine
        self.set_y(133)
        self.set_x(16)
        self.cell(
            0,
            h=5,
            txt="Famiglia di origine",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(45, 134, 3, 3, style="")  # Famiglia affidataria
        self.set_y(133)
        self.set_x(48)
        self.cell(
            0,
            h=5,
            txt="Famiglia affidataria",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(89, 134, 3, 3, style="")  # (Ex art.403)
        self.set_y(133)
        self.set_x(92)
        self.cell(0, h=5, txt="(Ex art.403)", border=0, ln=1, align="", fill=False, link="")
        self.rect(116, 134, 3, 3, style="")  # Genitori
        self.set_y(133)
        self.set_x(119)
        self.cell(0, h=5, txt="Genitori", border=0, ln=1, align="", fill=False, link="")
        self.rect(13, 140, 3, 3, style="")  # Famiglia Adottiva
        self.set_y(139)
        self.set_x(16)
        self.cell(
            0,
            h=5,
            txt="Famiglia Adottiva",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(45, 140, 3, 3, style="")  # Altro
        self.set_y(139)
        self.set_x(48)
        self.cell(0, h=5, txt="Altro", border=0, ln=1, align="", fill=False, link="")
        self.line(58, 143, 80, 143)
        self.rect(89, 142, 3, 3, style="")  # Comune di:
        self.set_y(141)
        self.set_x(92)
        self.cell(0, h=5, txt="Comune di :", border=0, ln=1, align="", fill=False, link="")
        self.line(112, 145, 200, 145)
        self.line(13, 150, 80, 150)
        self.rect(89, 147, 3, 3, style="")
        self.set_y(147)
        self.set_x(92)
        self.cell(
            0,
            h=5,
            txt="Forze dell'ordine",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(128, 147, 3, 3, style="")
        self.set_y(147)
        self.set_x(131)
        self.cell(0, h=5, txt="C.C.", border=0, ln=1, align="", fill=False, link="")
        self.rect(142, 147, 3, 3, style="")
        self.set_y(147)
        self.set_x(145)
        self.cell(0, h=5, txt="P.S.", border=0, ln=1, align="", fill=False, link="")
        self.rect(154, 147, 3, 3, style="")
        self.set_y(147)
        self.set_x(157)
        self.cell(0, h=5, txt="G.d.F.", border=0, ln=1, align="", fill=False, link="")
        self.rect(170, 147, 3, 3, style="")
        self.set_y(147)
        self.set_x(173)
        self.cell(0, h=5, txt="P.L. di:", border=0, ln=1, align="", fill=False, link="")
        self.line(187, 151, 200, 151)
        self.rect(13, 152, 3, 3, style="")
        self.set_y(152)
        self.set_x(16)
        self.cell(
            0,
            h=5,
            txt="Altra struttura specificare:",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.line(55, 157, 80, 157)
        self.set_y(152)
        self.set_x(90)
        self.cell(0, h=5, txt="Trib. Min. di", border=0, ln=1, align="", fill=False, link="")
        self.line(113, 157, 200, 157)
        self.line(13, 163, 80, 163)
        self.set_y(158)
        self.set_x(90)
        self.cell(0, h=5, txt="Giudice:", border=0, ln=1, align="", fill=False, link="")
        self.line(108, 163, 158, 163)
        self.set_y(159)
        self.set_x(158)
        self.cell(0, h=5, txt=" fasc.n°", border=0, ln=1, align="", fill=False, link="")
        self.line(170, 163, 200, 163)

    def add_to_section_4(self, minor):
        self.set_y(113)
        self.set_x(45)
        self.cell(
            0,
            h=5,
            txt=minor["disposal_date"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVuMono", size=8)
        self.set_y(113)
        self.set_x(95)
        self.cell(
            0,
            h=5,
            txt=minor["disposal_motivation"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVu", size=9.5)
        if minor["handicap"]["has_handicap"]:
            self.line(68, 120, 71, 123)
            self.line(68, 123, 71, 120)
            if "fisici" in minor["handicap"]["type"]:
                self.line(44, 120, 47, 123)
                self.line(44, 123, 47, 120)
            if "psichici" in minor["handicap"]["type"]:
                self.line(54, 120, 57, 123)
                self.line(54, 123, 57, 120)
        else:
            self.line(78, 120, 81, 123)
            self.line(78, 123, 81, 120)
        if minor["family_member"]["in_structure"]:
            self.line(128, 120, 131, 123)
            self.line(128, 123, 131, 120)
            if "madre" in minor["family_member"]["member"]:
                self.line(138, 120, 141, 123)
                self.line(138, 123, 141, 120)
            if "fratello/i" in minor["family_member"]["member"]:
                self.line(151, 120, 154, 123)
                self.line(151, 123, 154, 120)
            if "sorella/e" in minor["family_member"]["member"]:
                self.line(167, 120, 170, 123)
                self.line(167, 123, 170, 120)
        else:
            self.line(188, 120, 191, 123)
            self.line(188, 123, 191, 120)
        if minor["origin"]["type"] == "origin_family":
            self.line(13, 134, 16, 137)
            self.line(13, 137, 16, 134)
        if minor["origin"]["type"] == "foster_family":
            self.line(45, 134, 48, 137)
            self.line(45, 137, 48, 134)
        if "ex" in minor["placed_by"]["typology"]:
            self.line(89, 134, 92, 137)
            self.line(89, 137, 92, 134)
        if "parents" in minor["placed_by"]["typology"]:
            self.line(116, 134, 119, 137)
            self.line(116, 137, 119, 134)

        if minor["origin"]["type"] == "adoptive_family":
            self.line(13, 140, 16, 143)
            self.line(13, 143, 16, 140)
        if minor["origin"]["type"] == "other":
            self.line(45, 140, 48, 143)
            self.line(45, 143, 48, 140)
            if minor["origin"]["other"] != "":
                txt, rest_of_string = split_sentence(13, minor["origin"]["other"])
                self.set_font("DejaVuMono", size=8)
                self.set_y(139)
                self.set_x(57)
                self.cell(
                    0,
                    h=5,
                    txt=txt,
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
                self.set_y(146)
                self.set_x(13)
                self.cell(
                    0,
                    h=5,
                    txt=rest_of_string,
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
        if minor["origin"]["type"] == "other_struct":
            self.line(13, 152, 16, 155)
            self.line(13, 155, 16, 152)
            if minor["origin"]["detailed"] != "":
                self.set_font("DejaVuMono", size=8)
                txt, rest_of_string = split_sentence(15, minor["origin"]["detailed"])
                self.set_y(152)
                self.set_x(54)
                self.cell(
                    0,
                    h=5,
                    txt=txt,
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
                self.set_y(159)
                self.set_x(13)
                self.cell(
                    0,
                    h=5,
                    txt=rest_of_string,
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
        if "mun" in minor["placed_by"]["typology"]:
            self.line(89, 142, 92, 145)
            self.line(89, 145, 92, 142)
            if minor["placed_by"]["mun_of"] != "":
                self.set_y(141)
                self.set_x(112)
                self.cell(
                    0,
                    h=5,
                    txt=minor["placed_by"]["mun_of"],
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
        if "police" in minor["placed_by"]["typology"]:
            self.line(89, 147, 92, 150)
            self.line(89, 150, 92, 147)
            if minor["placed_by"]["type"] == "cc":
                self.line(128, 147, 131, 150)
                self.line(128, 150, 131, 147)
            elif minor["placed_by"]["type"] == "ps":
                self.line(142, 147, 145, 150)
                self.line(142, 150, 145, 147)
            elif minor["placed_by"]["type"] == "gdf":
                self.line(154, 147, 157, 150)
                self.line(154, 150, 157, 147)
            elif minor["placed_by"]["type"] == "pl":
                self.line(170, 147, 173, 150)
                self.line(170, 150, 173, 147)
                if minor["placed_by"]["pl_of"] != "":
                    self.set_y(147)
                    self.set_x(187)
                    self.cell(
                        0,
                        h=5,
                        txt=minor["placed_by"]["pl_of"],
                        border=0,
                        ln=1,
                        align="",
                        fill=False,
                        link="",
                    )
            elif minor["placed_by"]["type"] == "cc":
                self.line(89, 147, 92, 150)
                self.line(89, 150, 92, 147)
        if "police" in minor["placed_by"]["typology"]:
            if minor["placed_by"]["tri_min_of"] != "":
                self.set_y(152)
                self.set_x(116)
                self.cell(
                    0,
                    h=5,
                    txt=minor["placed_by"]["tri_min_of"],
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            if minor["placed_by"]["giudge"] != "":
                self.set_y(158)
                self.set_x(115)
                self.cell(
                    0,
                    h=5,
                    txt=minor["placed_by"]["giudge"],
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            if minor["placed_by"]["fasc_n"] != "":
                self.set_y(159)
                self.set_x(170)
                self.cell(
                    0,
                    h=5,
                    txt=minor["placed_by"]["fasc_n"],
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )

    def create_section_5(self):
        # SEZIONE 5
        self.set_font("DejaVu", "B", size=9)
        self.set_y(167)
        self.set_x(70)
        self.cell(
            0,
            h=5,
            txt="Parte riservata alla comunicazione semestrale",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(175)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="Incontri con i familiari:",
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVu")
        self.rect(60, 176, 3, 3, style="")
        self.set_x(63)
        self.cell(0, h=5, txt="padre", border=0, ln=0, align="", fill=False, link="")
        self.rect(78, 176, 3, 3, style="")
        self.set_x(81)
        self.cell(0, h=5, txt="madre", border=0, ln=0, align="", fill=False, link="")
        self.rect(96, 176, 3, 3, style="")
        self.set_x(99)
        self.cell(0, h=5, txt="fratelli", border=0, ln=0, align="", fill=False, link="")
        self.rect(113, 176, 3, 3, style="")
        self.set_x(116)
        self.cell(0, h=5, txt="nonni", border=0, ln=0, align="", fill=False, link="")
        self.rect(126, 176, 3, 3, style="")
        self.set_x(129)
        self.cell(0, h=5, txt="zii", border=0, ln=0, align="", fill=False, link="")
        self.set_y(183)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="In Comunità:",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(45, 184, 3, 3, style="")
        self.set_y(183)
        self.set_x(48)
        self.cell(0, h=5, txt="SI", border=0, ln=0, align="", fill=False, link="")
        self.rect(58, 184, 3, 3, style="")
        self.set_x(61)
        self.cell(0, h=5, txt="NO", border=0, ln=0, align="", fill=False, link="")
        self.set_x(71)
        self.cell(0, h=5, txt="frequenza", border=0, ln=0, align="", fill=False, link="")
        self.line(90, 187, 132, 187)
        self.set_x(136)
        self.cell(0, h=5, txt="Durata:", border=0, ln=0, align="", fill=False, link="")
        self.line(149, 187, 200, 187)
        self.set_y(190)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="Rientri in famiglia",
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.rect(55, 191, 3, 3, style="")
        self.set_x(58)
        self.cell(0, h=5, txt="SI", border=0, ln=0, align="", fill=False, link="")
        self.rect(65, 191, 3, 3, style="")
        self.set_x(68)
        self.cell(0, h=5, txt="NO", border=0, ln=0, align="", fill=False, link="")
        self.set_x(78)
        self.cell(0, h=5, txt="frequenza", border=0, ln=0, align="", fill=False, link="")
        self.line(95, 193, 137, 193)
        self.set_x(140)
        self.cell(0, h=5, txt="Durata:", border=0, ln=0, align="", fill=False, link="")
        self.line(153, 193, 200, 193)
        self.set_font("DejaVu", "B")
        self.set_y(197)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="Incontri con: famiglie indicate da",
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVu")
        self.rect(83, 197, 3, 3, style="")
        self.set_x(86)
        self.cell(0, h=5, txt="Serv. Sociale", border=0, ln=0, align="", fill=False, link="")
        self.rect(113, 197, 3, 3, style="")
        self.set_x(116)
        self.cell(0, h=5, txt="Resp. Comunità", border=0, ln=0, align="", fill=False, link="")
        self.rect(143, 197, 3, 3, style="")
        self.set_x(146)
        self.cell(0, h=5, txt="T.M.", border=0, ln=0, align="", fill=False, link="")
        self.rect(166, 197, 3, 3, style="")
        self.set_x(169)
        self.cell(
            0,
            h=5,
            txt="Famiglie di volontari",
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.set_y(203)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="In Comunità:",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(45, 204, 3, 3, style="")
        self.set_y(203)
        self.set_x(48)
        self.cell(0, h=5, txt="SI", border=0, ln=0, align="", fill=False, link="")
        self.rect(58, 204, 3, 3, style="")
        self.set_x(61)
        self.cell(0, h=5, txt="NO", border=0, ln=0, align="", fill=False, link="")
        self.set_x(71)
        self.cell(0, h=5, txt="frequenza", border=0, ln=0, align="", fill=False, link="")
        self.line(90, 207, 132, 207)
        self.set_x(136)
        self.cell(0, h=5, txt="Durata:", border=0, ln=0, align="", fill=False, link="")
        self.line(149, 207, 200, 207)
        self.set_y(210)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="Presso il domicilio",
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.rect(55, 211, 3, 3, style="")
        self.set_x(58)
        self.cell(0, h=5, txt="SI", border=0, ln=0, align="", fill=False, link="")
        self.rect(65, 211, 3, 3, style="")
        self.set_x(68)
        self.cell(0, h=5, txt="NO", border=0, ln=0, align="", fill=False, link="")
        self.set_x(78)
        self.cell(0, h=5, txt="frequenza", border=0, ln=0, align="", fill=False, link="")
        self.line(95, 214, 137, 214)
        self.set_x(140)
        self.cell(0, h=5, txt="Durata:", border=0, ln=0, align="", fill=False, link="")
        self.line(153, 214, 200, 214)
        self.set_font("DejaVu", "B")
        self.set_y(221)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="Visite del Tutore",
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVu")
        self.rect(43, 222, 3, 3, style="")
        self.set_x(46)
        self.cell(0, h=5, txt="SI", border=0, ln=0, align="", fill=False, link="")
        self.rect(53, 222, 3, 3, style="")
        self.set_x(56)
        self.cell(0, h=5, txt="NO", border=0, ln=0, align="", fill=False, link="")
        self.set_x(66)
        self.cell(0, h=5, txt="frequenza", border=0, ln=0, align="", fill=False, link="")
        self.line(85, 225, 108, 225)
        self.set_x(109)
        self.set_font("DejaVu", "B")
        self.cell(
            0,
            h=5,
            txt="Visite dell'ass. soc.",
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVu")
        self.rect(142, 222, 3, 3, style="")
        self.set_x(145)
        self.cell(0, h=5, txt="SI", border=0, ln=0, align="", fill=False, link="")
        self.rect(150, 222, 3, 3, style="")
        self.set_x(153)
        self.cell(0, h=5, txt="NO", border=0, ln=0, align="", fill=False, link="")
        self.set_x(160)
        self.cell(0, h=5, txt="frequenza", border=0, ln=0, align="", fill=False, link="")
        self.line(176, 225, 200, 225)
        self.set_font("DejaVu", "B")
        self.set_y(229)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="Percorso Evolutivo",
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVu")
        self.line(47, 233, 200, 233)
        self.line(13, 238, 200, 238)

    def add_to_section_5(self, semestral_comunication):
        if "padre" in semestral_comunication["family_members_meeting"]["member"]:
            self.line(60, 176, 63, 179)
            self.line(60, 179, 63, 176)
        if "madre" in semestral_comunication["family_members_meeting"]["member"]:
            self.line(78, 176, 81, 179)
            self.line(78, 179, 81, 176)
        if "fratelli" in semestral_comunication["family_members_meeting"]["member"]:
            self.line(96, 176, 99, 179)
            self.line(96, 179, 99, 176)
        if "nonni" in semestral_comunication["family_members_meeting"]["member"]:
            self.line(113, 176, 116, 179)
            self.line(113, 179, 116, 176)
        if "zii" in semestral_comunication["family_members_meeting"]["member"]:
            self.line(126, 176, 129, 179)
            self.line(126, 179, 129, 176)
        if semestral_comunication["family_members_meeting"]["in_community"]:
            self.line(45, 184, 48, 187)
            self.line(45, 187, 48, 184)
            if semestral_comunication["family_members_meeting"]["in_community_freq"] != "":
                self.set_y(183)
                self.set_x(87)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["family_members_meeting"]["in_community_freq"],
                    border=0,
                    ln=0,
                    align="",
                    fill=False,
                    link="",
                )
            if semestral_comunication["family_members_meeting"]["in_community_duration"] != "":
                self.set_y(183)
                self.set_x(147)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["family_members_meeting"]["in_community_duration"],
                    border=0,
                    ln=0,
                    align="",
                    fill=False,
                    link="",
                )
        else:
            self.line(58, 184, 61, 187)
            self.line(58, 187, 61, 184)
        if semestral_comunication["family_members_meeting"]["return_to_family"]:
            self.line(55, 191, 58, 194)
            self.line(55, 194, 58, 191)
            if semestral_comunication["family_members_meeting"]["return_to_family_freq"] != "":
                self.set_y(189)
                self.set_x(93)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["family_members_meeting"]["return_to_family_freq"],
                    border=0,
                    ln=0,
                    align="",
                    fill=False,
                    link="",
                )
            if semestral_comunication["family_members_meeting"]["return_to_family_duration"] != "":
                self.set_y(189)
                self.set_x(151)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["family_members_meeting"]["return_to_family_duration"],
                    border=0,
                    ln=0,
                    align="",
                    fill=False,
                    link="",
                )
        else:
            self.line(65, 191, 68, 194)
            self.line(65, 194, 68, 191)
        if semestral_comunication["family_members_meeting_by"]["name"] == "social_service":
            self.line(83, 197, 86, 200)
            self.line(83, 200, 86, 197)
        if semestral_comunication["family_members_meeting_by"]["name"] == "community_resp":
            self.line(113, 197, 116, 200)
            self.line(113, 200, 116, 197)
        if semestral_comunication["family_members_meeting_by"]["name"] == "tm":
            self.line(143, 197, 146, 200)
            self.line(143, 200, 146, 197)
        if semestral_comunication["family_members_meeting_by"]["name"] == "volunteers_family":
            self.line(166, 197, 169, 200)
            self.line(166, 200, 169, 197)
        if semestral_comunication["family_members_meeting_by"]["in_community"]:
            self.line(45, 204, 48, 207)
            self.line(45, 207, 48, 204)
            if semestral_comunication["family_members_meeting_by"]["in_community_freq"] != "":
                self.set_y(203)
                self.set_x(87)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["family_members_meeting_by"]["in_community_freq"],
                    border=0,
                    ln=0,
                    align="",
                    fill=False,
                    link="",
                )
            if semestral_comunication["family_members_meeting_by"]["in_community_duration"] != "":
                self.set_y(203)
                self.set_x(147)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["family_members_meeting_by"]["in_community_duration"],
                    border=0,
                    ln=0,
                    align="",
                    fill=False,
                    link="",
                )
        else:
            self.line(58, 204, 61, 207)
            self.line(58, 207, 61, 204)
        if semestral_comunication["family_members_meeting_by"]["return_home"]:
            self.line(55, 211, 58, 214)
            self.line(55, 214, 58, 211)
            if semestral_comunication["family_members_meeting_by"]["return_home_freq"] != "":
                self.set_y(210)
                self.set_x(93)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["family_members_meeting_by"]["return_home_freq"],
                    border=0,
                    ln=0,
                    align="",
                    fill=False,
                    link="",
                )
            if semestral_comunication["family_members_meeting_by"]["return_home_duration"] != "":
                self.set_y(210)
                self.set_x(151)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["family_members_meeting_by"]["return_home_duration"],
                    border=0,
                    ln=0,
                    align="",
                    fill=False,
                    link="",
                )
        else:
            self.line(65, 211, 68, 214)
            self.line(65, 214, 68, 211)

        if semestral_comunication["legal_guardian_visit"]:
            self.line(43, 222, 46, 225)
            self.line(43, 225, 46, 222)
            if semestral_comunication["legal_guardian_visit_freq"] != "":
                self.set_y(221)
                self.set_x(83)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["legal_guardian_visit_freq"],
                    border=0,
                    ln=0,
                    align="",
                    fill=False,
                    link="",
                )
        else:
            self.line(53, 222, 56, 225)
            self.line(53, 225, 56, 222)

        if semestral_comunication["ass_soc_visit"]:
            self.line(142, 222, 145, 225)
            self.line(142, 225, 145, 222)
            if semestral_comunication["ass_soc_visit_freq"] != "":
                self.set_y(221)
                self.set_x(175)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["ass_soc_visit_freq"],
                    border=0,
                    ln=0,
                    align="",
                    fill=False,
                    link="",
                )
        else:
            self.line(150, 222, 153, 225)
            self.line(150, 225, 153, 222)
        if semestral_comunication["evolutionary_path"] != "":
            txt, rest_of_string = split_sentence(90, semestral_comunication["evolutionary_path"])
            self.set_font("DejaVuMono", size=8)
            self.set_y(229)
            self.set_x(47)
            self.cell(
                0,
                h=5,
                txt=txt,
                border=0,
                ln=0,
                align="",
                fill=False,
                link="",
            )
            if len(semestral_comunication["evolutionary_path"]) > 90:
                self.set_y(234)
                self.set_x(13)
                self.cell(
                    0,
                    h=5,
                    txt=rest_of_string,
                    border=0,
                    ln=0,
                    align="",
                    fill=False,
                    link="",
                )
            self.set_font("DejaVu", size=9.5)

    def create_footer(self):
        # SEZIONE 6
        self.set_font("DejaVu", "B")
        self.set_y(239)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="Aspettattive del Minore ",
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.set_x(120)
        self.cell(
            0,
            h=5,
            txt="*Obiettivo:",
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.set_font("DejaVu")
        self.rect(15, 246, 3, 3, style="")
        self.set_y(245)
        self.set_x(18)
        self.cell(
            0,
            h=5,
            txt="Rientri in Famiglia",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(15, 252, 3, 3, style="")
        self.set_y(251)
        self.set_x(18)
        self.cell(
            0,
            h=5,
            txt="Affido Familiare",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(15, 257, 3, 3, style="")
        self.set_y(256)
        self.set_x(18)
        self.cell(
            0,
            h=5,
            txt="Adozione",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(47, 246, 3, 3, style="")
        self.set_y(245)
        self.set_x(50)
        self.cell(
            0,
            h=5,
            txt="Percorsi di Autonomia",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(47, 252, 3, 3, style="")
        self.set_y(251)
        self.set_x(50)
        self.cell(
            0,
            h=5,
            txt="Non Valutabile",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(47, 257, 3, 3, style="")
        self.set_y(256)
        self.set_x(50)
        self.cell(
            0,
            h=5,
            txt="Altro",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.line(58, 260, 119, 260)
        self.rect(122, 246, 3, 3, style="")
        self.set_y(245)
        self.set_x(125)
        self.cell(
            0,
            h=5,
            txt="Rientri in Famiglia",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(122, 252, 3, 3, style="")
        self.set_y(251)
        self.set_x(125)
        self.cell(
            0,
            h=5,
            txt="Affido Familiare",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(122, 257, 3, 3, style="")
        self.set_y(256)
        self.set_x(125)
        self.cell(
            0,
            h=5,
            txt="Adozione",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(155, 246, 3, 3, style="")
        self.set_y(245)
        self.set_x(158)
        self.cell(
            0,
            h=5,
            txt="Percorsi di Autonomia",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(155, 252, 3, 3, style="")
        self.set_y(251)
        self.set_x(158)
        self.cell(
            0,
            h=5,
            txt="Non Valutabile",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.rect(155, 257, 3, 3, style="")
        self.set_font("DejaVu", "B")
        self.set_y(256)
        self.set_x(158)
        self.cell(
            0,
            h=5,
            txt="Altro",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_line_width(0.4)
        self.line(168, 260, 196, 260)
        self.line(14, 268, 101, 268)
        self.set_font("DejaVu", size=8)
        self.set_y(262)
        self.set_x(103)
        self.cell(
            0,
            h=5,
            txt="*Concordato/i con l'assistente sociale del Comune di provenienza del minore",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_line_width(0.2)
        self.set_y(269)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="N.B.    Al momento dell'ingresso e delle dimissioni si dovrà allegare il provvedimento "
            "dell'Autorità che li ha disposti. Ulteriori informazioni relative al",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(272)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="minore potranno essere annotate sul retro. Da compilare in stampatello. Rispondere a tutte "
            "le voci. Barrare i campi per i quali non si conoscono le",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_y(275)
        self.set_x(13)
        self.cell(
            0,
            h=5,
            txt="informazioni.",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_font(size=11)
        self.set_y(287)
        self.set_x(16)
        self.cell(
            0,
            h=5,
            txt="Data",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.line(27, 292, 67, 292)
        self.set_font(size=10)
        self.set_y(281)
        self.set_x(155)
        self.cell(
            0,
            h=5,
            txt="Firma del coordinatore",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.line(150, 292, 198, 292)

    def add_to_footer(self, semestral_comunication):
        if "family_returns" in semestral_comunication["minor_expectation"]["type"]:
            self.line(15, 246, 18, 249)
            self.line(15, 249, 18, 246)
        if "family_foster_care" in semestral_comunication["minor_expectation"]["type"]:
            self.line(15, 252, 18, 255)
            self.line(15, 255, 18, 252)
        if "adoption" in semestral_comunication["minor_expectation"]["type"]:
            self.line(15, 257, 18, 260)
            self.line(15, 260, 18, 257)
        if "autonomy_routes" in semestral_comunication["minor_expectation"]["type"]:
            self.line(47, 246, 50, 249)
            self.line(47, 249, 50, 246)
        if "not_evaluable" in semestral_comunication["minor_expectation"]["type"]:
            self.line(47, 252, 50, 255)
            self.line(47, 255, 50, 252)
        if "other" in semestral_comunication["minor_expectation"]["type"]:
            self.line(47, 257, 50, 260)
            self.line(47, 260, 50, 257)
            if semestral_comunication["minor_expectation"]["other"] != "":
                self.set_font("DejaVu", size=7)
                self.set_y(256)
                self.set_x(57)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["minor_expectation"]["other"],
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
        if "family_returns" in semestral_comunication["target"]["type"]:
            self.line(122, 246, 125, 249)
            self.line(122, 249, 125, 246)
        if "family_foster_care" in semestral_comunication["target"]["type"]:
            self.line(122, 252, 125, 255)
            self.line(122, 255, 125, 252)
        if "adoption" in semestral_comunication["target"]["type"]:
            self.line(122, 257, 125, 260)
            self.line(122, 260, 125, 257)
        if "autonomy_routes" in semestral_comunication["target"]["type"]:
            self.line(155, 246, 158, 249)
            self.line(155, 249, 158, 246)
        if "not_evaluable" in semestral_comunication["target"]["type"]:
            self.line(155, 252, 158, 255)
            self.line(155, 255, 158, 252)
        if "other" in semestral_comunication["target"]["type"]:
            self.line(155, 257, 158, 260)
            self.line(155, 260, 158, 257)
            if semestral_comunication["target"]["other"] != "":
                self.set_font("DejaVu", size=7)
                self.set_y(256)
                self.set_x(167)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["target"]["other"][:23],
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
                self.set_y(263)
                self.set_x(13)
                self.cell(
                    0,
                    h=5,
                    txt=semestral_comunication["target"]["other"][23:],
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )

        self.set_y(287)
        self.set_x(30)
        self.cell(
            0,
            h=5,
            txt=semestral_comunication["date"],
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )

    def create_document(self, info):
        self.create_section_1()
        self.create_section_2()
        self.create_section_3()
        self.create_section_4()
        self.create_section_5()
        self.create_footer()
        if info:
            self.add_data_to_document(info)

    def create_secondPage(self, info):
        self.create_section_2page()
        if info:
            self.add_data_to_secondPage(info)

    def add_data_to_document(self, info):
        self.add_to_section_1(info["community"])
        self.add_to_section_3(info["minor"])
        self.add_to_section_4(info["minor"])
        self.add_to_section_5(info["semestral_comunication"])
        self.add_to_footer(info["semestral_comunication"])

    def add_data_to_secondPage(self, info):
        self.add_to_section_2page(info)


def checkField(field, data):
    return data[field] if field in data else ""


def generate_minor_information_sheet(info=None):
    pdf = PDF()
    pdf.add_page()
    fonts = [
        ("DejaVu", "", FONT_DEJAVU_SANS_CONDENSED),
        ("DejaVu", "B", FONT_DEJAVU_SANS_CONDENSED_BOLD),
        ("DejaVu", "I", FONT_DEJAVU_SANS_CONDENSED_OBLIQUE),
        ("DejaVu", "BI", FONT_DEJAVU_SANS_CONDENSED_BOLD_OBLIQUE),
        ("DejaVuMono", "", FONT_DEJAVU_SANS_MONO),
        ("DejaVuMono", "B", FONT_DEJAVU_SANS_MONO_BOLD),
        ("DejaVuMono", "I", FONT_DEJAVU_SANS_MONO_OBLIQUE),
        ("DejaVuMono", "BI", FONT_DEJAVU_SANS_MONO_BOLD_OBLIQUE),
    ]
    for font in fonts:
        pdf.add_font(font[0], font[1], font[2], uni=True)
    pdf.set_font("DejaVu", size=11)
    pdf.set_margins(13, 5)
    pdf.set_auto_page_break(False)
    pdf.create_document(info)
    pdf.add_page()
    pdf.set_font("DejaVu", size=11)
    pdf.set_margins(13, 5)
    pdf.create_secondPage(info.get("semestral_comunication").get("added_section_evolutionary_path"))
    return base64.b64encode(pdf.output(dest="S")).decode()


def archive_minor_information_sheet(db=None, info_children=None, info=None):
    pdf = PDF()
    pdf.add_page()
    fonts = [
        ("DejaVu", "", FONT_DEJAVU_SANS_CONDENSED),
        ("DejaVu", "B", FONT_DEJAVU_SANS_CONDENSED_BOLD),
        ("DejaVu", "I", FONT_DEJAVU_SANS_CONDENSED_OBLIQUE),
        ("DejaVu", "BI", FONT_DEJAVU_SANS_CONDENSED_BOLD_OBLIQUE),
        ("DejaVuMono", "", FONT_DEJAVU_SANS_MONO),
        ("DejaVuMono", "B", FONT_DEJAVU_SANS_MONO_BOLD),
        ("DejaVuMono", "I", FONT_DEJAVU_SANS_MONO_OBLIQUE),
        ("DejaVuMono", "BI", FONT_DEJAVU_SANS_MONO_BOLD_OBLIQUE),
    ]
    for font in fonts:
        pdf.add_font(font[0], font[1], font[2], uni=True)
    pdf.set_font("DejaVu", size=11)
    pdf.set_margins(13, 5)
    pdf.set_auto_page_break(False)
    pdf.create_document(info)
    pdf.add_page()
    pdf.set_font("DejaVu", size=11)
    pdf.set_margins(13, 5)
    pdf.create_secondPage(info.get("semestral_comunication").get("added_section_evolutionary_path"))
    pdf_content = pdf.output(dest="S")
    pdf_content_base64 = base64.b64encode(pdf_content).decode("utf-8")
    date = datetime.strptime(info_children.get("info_sheet").get("semestral_comunication").get("date"), "%d/%m/%Y")
    document = {
        "id_children": info_children.get("_id"),
        "name": info_children.get("name"),
        "surname": info_children.get("surname"),
        "fiscal_code": info_children.get("fiscal_code"),
        "archive_date": date,
        "pdf_data": pdf_content_base64,
    }
    result = db["minor_info_sheets"].insert_one(document)
    return result


def generate_ai_report_pdf(info=None):
    pdf = PDF()
    pdf.add_page()
    fonts = [
        ("DejaVu", "", FONT_DEJAVU_SANS_CONDENSED),
        ("DejaVu", "B", FONT_DEJAVU_SANS_CONDENSED_BOLD),
        ("DejaVu", "I", FONT_DEJAVU_SANS_CONDENSED_OBLIQUE),
        ("DejaVu", "BI", FONT_DEJAVU_SANS_CONDENSED_BOLD_OBLIQUE),
    ]
    for font in fonts:
        pdf.add_font(font[0], font[1], font[2], uni=True)
    pdf.set_font("DejaVu", size=11)
    pdf.set_margins(13, 5)
    pdf.set_auto_page_break(True, margin=15)

    pdf.cell(0, 10, f"Rapporto Operatore: {info['operator']['name']} {info['operator']['surname']}", 0, 1, "C")
    pdf.cell(0, 10, f"Periodo: {info['start_date']} - {info['end_date']}", 0, 1, "C")
    pdf.ln(10)

    pdf.multi_cell(0, 5, info["ai_report"])

    return base64.b64encode(pdf.output(dest="S")).decode()
