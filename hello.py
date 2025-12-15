import math
s_1 = 4478.955
s_2 = 4184.595
c = 456
odchylka = 0.5
odchylka_OVA = 6
odchylka_BER = 7
odchylka_ova = [odchylka_OVA-odchylka, odchylka_OVA, odchylka_OVA+odchylka]
odchylka_ber = [odchylka_BER-odchylka, odchylka_BER, odchylka_BER+odchylka]
hodnoty = []
for x in range(3):
    alpha = 127.86079489
    alpha_2 = alpha - odchylka_ova[x]
    beta = 47.52885405
    beta_2 = beta - odchylka_ber[x]
    alpha_rad = alpha*math.pi/180
    alpha_2_rad = alpha_2*math.pi/180
    beta_rad = beta*math.pi/180
    s1 = (math.sin(alpha_rad)*s_1-math.sin(alpha_2_rad)*(c * math.sin(alpha_rad)/math.sin(alpha_rad+beta_rad)))**2
    s2 = (math.cos(alpha_rad)*s_1-math.cos(alpha_2_rad)*(c*math.sin(alpha_rad)/math.sin(alpha_rad+beta_rad)))**2
    #s = \sqrt{(\sin \alpha \cdot s_1-\sin \alpha_2 \cdot \frac{c \cdot \sin \alpha}{\sin (\alpha+\beta)})^2+(\cos \alpha \cdot s_1+\cos \alpha_2 \cdot \frac{c \cdot \sin \alpha}{\sin (\alpha+\beta)})^2}\\
    print(s1)
    print(s2)
    s = math.sqrt(s2+s1)
    hodnoty.append(s)
print(f"Vzdálenost je přibližně {hodnoty[1]}km")
print(f"Odchylka je {hodnoty[2]- hodnoty[0]}km")