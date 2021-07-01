from random import randint
media_atendimento = media_fila = 0

entidade = int(input("Digite o número de entidades: "))
i = i1 = i2 = soma = 0
vs1 = [] 
vs2 = []
vs1a = []
te = []
ts = []
tf = []
#print("ENT VS1 VS1A VS2")
for i in range(entidade):
    i1 = randint(1,20)
    i2 = randint(1,20)
    soma += i1
    vs1.append(i1)
    vs2.append(i2)
    vs1a.append(soma)
    media_atendimento = media_atendimento + vs2[i]
    #print("{:>2} {:>3} {:>4} {:>3}".format(i+1,vs1[i],vs1a[i],vs2[i]))

i = 0
tf.append(0)
ts.append(0)
print ("ENT. TC   TF  TE  TA   TS")
for i in range(entidade):
    te.append(vs1a[i] + tf[i])
    ts.append(vs2[i] + te[i])
    media_fila = media_fila + tf[i]
    print("{:>2} {:>4} {:>4} {:>3} {:>3} {:>4}".format(i+1,vs1a[i],tf[i],te[i],vs2[i],ts[i]))
    tf.append(ts[i+1] - vs1a[i])

print("\n")
media_fila = media_fila/10 
media_atendimento = media_atendimento/10
print("Tempo médio de atendimento: %.2f"%media_atendimento)
print("Tempo médio de fila: %.2f"%media_fila)

print("\n")
print("     FILA\n")
print("ENT. TC   TF  TE")
for i in range(entidade):
    print("{:>2} {:>4} {:>4} {:>3}".format(i+1,vs1a[i], tf[i], te[i]))

print("\n")
print("ATENDIMENTO CS1\n")
print("ENT. TI   TA  TT")
for i in range(entidade):
    print("{:>2} {:>4} {:>4} {:>3}".format(i+1, te[i], vs2[i], ts[i]))
