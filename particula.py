import numpy as np
import random as rd

class Particula:
    
    def __init__(self, pos, velocidade, raio, massa, reatividade):
        """inicializar o objeto partícula
        
        Args:
        posição da partícula
        velocidade da particula
        raio da particula
        massa da particula
        """
        self.existe = True
        self.massa = massa
        self.raio = raio
        self.reatividade = reatividade
        
        # estado atual da partícula
        self.pos = np.array(pos)
        self.velocidade = np.array(velocidade)
        self.tipo = '0'
        self.lista_tipo = ['0']
        
        # estado gravado ao longo de toda a simulação
        self.trapos = [np.copy(self.pos)]
        self.travel = [np.copy(self.velocidade)]
        self.travel_mag = [np.linalg.norm(np.copy(self.velocidade))]
        self.num_col = 0
        self.lista_existe = [1]
        
    def update(self, step):
        """Calcula a posição seguinte com base na velocidade"""
        self.pos += step * self.velocidade
        self.trapos.append(np.copy(self.pos)) 
        self.travel.append(np.copy(self.velocidade)) 
        self.travel_mag.append(np.linalg.norm(np.copy(self.velocidade))) 
        self.lista_tipo.append(self.tipo)
        if self.existe == True:
            self.lista_existe.append(1)
        else:
            self.lista_existe.append(0)


        
    def checar_col(self, particula):
        """Checa se houve colisão com alguma partícula"""
        r1, r2 = self.raio, particula.raio
        x1, x2 = self.pos, particula.pos
        di = x2-x1
        norm = np.linalg.norm(di)
        if self.existe == True and particula.existe == True and norm-(r1+r2)*1.1 < 0:
            return True
        else:
            return False

    def calc_col(self, particula, step):
        """calcula o resultado da colisão"""
        m1, m2 = self.massa, particula.massa
        r1, r2 = self.raio, particula.raio
        v1, v2 = self.velocidade, particula.velocidade
        x1, x2 = self.pos, particula.pos
        di = x2-x1
        norm = np.linalg.norm(di)
        react = rd.random()            
        if norm-(r1+r2)*1.1 < step*abs(np.dot(v1-v2, di))/norm:
            if (self.reatividade + particula.reatividade)/2 < react or self.tipo == 'r' or particula.tipo == 'r':
                self.num_col += 1
                particula.num_col += 1
                self.velocidade = v1 - 2. * m2/(m1+m2) * np.dot(v1-v2, di) / (np.linalg.norm(di)**2.) * di
                particula.velocidade = v2 - 2. * m1/(m2+m1) * np.dot(v2-v1, (-di)) / (np.linalg.norm(di)**2.) * (-di)
            if (self.reatividade + particula.reatividade)/2 >= react and self.tipo == '0' and particula.tipo == '0':
                self.tipo = 'r'
                self.massa = m1+m2
                self.raio = np.sqrt(r1**2 + r2**2)
                self.velocidade = np.array([(m1*v1[0] + m2*v2[0])/(m1+m2), (m1*v1[1] + m2*v2[1])/(m1+m2)])
                particula.existe = False

    def calc_col_parede(self, step, tamanho):
        """Calcula colisão com a parede
        Args:
        tamanho do step de tempo
        tamanho da caixa
        """
        r, v, x = self.raio, self.velocidade, self.pos
        projx = step*abs(np.dot(v,np.array([1.,0.])))
        projy = step*abs(np.dot(v,np.array([0.,1.])))
        if abs(x[0])-r < projx or abs(tamanho-x[0])-r < projx:
            self.velocidade[0] *= -1
        if abs(x[1])-r < projy or abs(tamanho-x[1])-r < projy:
            self.velocidade[1] *= -1.
            

            
class Particula2:
    
    """Teste para fazer com catálise, se estiver 
    funcionando e o desafio 1 e 2 ainda estiverem funcionando, 
    essa vira a classe Particula"""
    
    def __init__(self, pos, velocidade, raio, massa, ecmin, catalise = False):
        """inicializar o objeto partícula
        
        Args:
        posição da partícula
        velocidade da particula
        raio da particula
        massa da particula
        """
        self.existe = True
        self.massa = massa
        self.raio = raio
#        self.reatividade = reatividade
        
        # estado atual da partícula
        self.pos = np.array(pos)
        self.velocidade = np.array(velocidade)
        self.tipo = '0'
        self.lista_tipo = ['0']
        self.Ec = massa*np.linalg.norm(velocidade)**2/2
        self.EcMin = ecmin
        
        # estado gravado ao longo de toda a simulação
        self.trapos = [np.copy(self.pos)]
        self.travel = [np.copy(self.velocidade)]
        self.travel_mag = [np.linalg.norm(np.copy(self.velocidade))]
        self.num_col = 0
        self.lista_existe = [1]
        
        #catalise:
        self.catalise = catalise
            
        
    def update(self, step):
        """Calcula a posição seguinte com base na velocidade"""
        self.pos += step * self.velocidade
        self.trapos.append(np.copy(self.pos)) 
        self.travel.append(np.copy(self.velocidade)) 
        self.travel_mag.append(np.linalg.norm(np.copy(self.velocidade))) 
        self.lista_tipo.append(self.tipo)
        self.Ec = self.massa*np.linalg.norm(self.velocidade)**2/2
        if self.existe == True:
            self.lista_existe.append(1)
        else:
            self.lista_existe.append(0)


        
    def checar_col(self, particula):
        """Checa se houve colisão com alguma partícula"""
        r1, r2 = self.raio, particula.raio
        x1, x2 = self.pos, particula.pos
        di = x2-x1
        norm = np.linalg.norm(di)
        if self.existe == True and particula.existe == True and norm-(r1+r2)*1.1 < 0:
            return True
        else:
            return False

    def calc_col(self, particula, step):
        """calcula o resultado da colisão"""
        m1, m2 = self.massa, particula.massa
        r1, r2 = self.raio, particula.raio
        v1, v2 = self.velocidade, particula.velocidade
        x1, x2 = self.pos, particula.pos
        di = x2-x1
        norm = np.linalg.norm(di)
        react = rd.random()            
        if norm-(r1+r2)*1.1 < step*abs(np.dot(v1-v2, di))/norm:
            if (self.Ec + particula.Ec) < self.EcMin +particula.EcMin or self.tipo == 'r' or particula.tipo == 'r':
                self.num_col += 1
                particula.num_col += 1
                self.velocidade = v1 - 2. * m2/(m1+m2) * np.dot(v1-v2, di) / (np.linalg.norm(di)**2.) * di
                particula.velocidade = v2 - 2. * m1/(m2+m1) * np.dot(v2-v1, (-di)) / (np.linalg.norm(di)**2.) * (-di)
            if (self.Ec + particula.Ec) >= self.EcMin +particula.EcMin and self.tipo == '0' and particula.tipo == '0':
                self.tipo = 'r'
                self.massa = m1+m2
                self.raio = np.sqrt(r1**2 + r2**2)
                self.velocidade = np.array([(m1*v1[0] + m2*v2[0])/(m1+m2), (m1*v1[1] + m2*v2[1])/(m1+m2)])
                particula.existe = False

    def calc_col_parede(self, step, tamanho):
        """Calcula colisão com a parede
        Args:
        tamanho do step de tempo
        tamanho da caixa
        """
        r, v, x = self.raio, self.velocidade, self.pos
        projx = step*abs(np.dot(v,np.array([1.,0.])))
        projy = step*abs(np.dot(v,np.array([0.,1.])))
        if abs(x[0])-r < projx or abs(tamanho-x[0])-r < projx:
            self.velocidade[0] *= -1
        if abs(x[1])-r < projy or abs(tamanho-x[1])-r < projy:
            self.velocidade[1] *= -1.
            
        ### CATALISE pela parete direita:
        if abs(tamanho-x[0])-r < projx and self.catalise != False:
            self.EcMin = self.EcMin*self.catalise

            
class Particula3:
    
    """Teste para fazer com catálise, se estiver 
    funcionando e o desafio 1 e 2 ainda estiverem funcionando, 
    essa vira a classe Particula"""
    
    def __init__(self, pos, velocidade, raio, massa, ecmin, catalise = False):
        """inicializar o objeto partícula
        
        Args:
        posição da partícula
        velocidade da particula
        raio da particula
        massa da particula
        """
        self.existe = True
        self.massa = massa
        self.raio = raio
#        self.reatividade = reatividade
        
        # estado atual da partícula
        self.pos = np.array(pos)
        self.velocidade = np.array(velocidade)
        self.tipo = '0'
        self.lista_tipo = ['0']
        self.Ec = massa*np.linalg.norm(velocidade)**2/2
        self.EcMin = ecmin
        
        # estado gravado ao longo de toda a simulação
        self.trapos = [np.copy(self.pos)]
        self.travel = [np.copy(self.velocidade)]
        self.travel_mag = [np.linalg.norm(np.copy(self.velocidade))]
        self.num_col = 0
        self.lista_existe = [1]
        
        #catalise:
        self.catalise = catalise
            
        
    def update(self, step):
        """Calcula a posição seguinte com base na velocidade"""
        self.pos += step * self.velocidade
        self.trapos.append(np.copy(self.pos)) 
        self.travel.append(np.copy(self.velocidade)) 
        self.travel_mag.append(np.linalg.norm(np.copy(self.velocidade))) 
        self.lista_tipo.append(self.tipo)
        self.Ec = self.massa*np.linalg.norm(self.velocidade)**2/2
        if self.existe == True:
            self.lista_existe.append(1)
        else:
            self.lista_existe.append(0)


        
    def checar_col(self, particula):
        """Checa se houve colisão com alguma partícula"""
        r1, r2 = self.raio, particula.raio
        x1, x2 = self.pos, particula.pos
        di = x2-x1
        norm = np.linalg.norm(di)
        if self.existe == True and particula.existe == True and norm-(r1+r2)*1.1 < 0:
            return True
        else:
            return False

    def calc_col(self, particula, step):
        """calcula o resultado da colisão"""
        m1, m2 = self.massa, particula.massa
        r1, r2 = self.raio, particula.raio
        v1, v2 = self.velocidade, particula.velocidade
        x1, x2 = self.pos, particula.pos
        di = x2-x1
        norm = np.linalg.norm(di)
        react = rd.random()            
        if norm-(r1+r2)*1.1 < step*abs(np.dot(v1-v2, di))/norm:
            if (self.Ec + particula.Ec) < self.EcMin +particula.EcMin or self.tipo == 'r' or particula.tipo == 'r':
                self.num_col += 1
                particula.num_col += 1
                self.velocidade = v1 - 2. * m2/(m1+m2) * np.dot(v1-v2, di) / (np.linalg.norm(di)**2.) * di
                particula.velocidade = v2 - 2. * m1/(m2+m1) * np.dot(v2-v1, (-di)) / (np.linalg.norm(di)**2.) * (-di)
            if (self.Ec + particula.Ec) >= self.EcMin +particula.EcMin and self.tipo == '0' and particula.tipo == '0':
                self.tipo = 'r'
                self.massa = m1+m2
                self.raio = np.sqrt(r1**2 + r2**2)
                self.velocidade = np.array([(m1*v1[0] + m2*v2[0])/(m1+m2), (m1*v1[1] + m2*v2[1])/(m1+m2)])
                particula.existe = False

    def calc_col_parede(self, step, tamanho):
        """Calcula colisão com a parede
        Args:
        tamanho do step de tempo
        tamanho da caixa
        """
        r, v, x = self.raio, self.velocidade, self.pos
        projx = step*abs(np.dot(v,np.array([1.,0.])))
        projy = step*abs(np.dot(v,np.array([0.,1.])))
        if abs(x[0])-r < projx or abs(tamanho-x[0])-r < projx:
            self.velocidade[0] *= -1
        if abs(x[1])-r < projy or abs(tamanho-x[1])-r < projy:
            self.velocidade[1] *= -1.
            
        ### CATALISE pela parete direita:
        if self.catalise != False:
            if abs(x[0])-r < projx or abs(tamanho-x[0])-r < projx:
                self.EcMin = self.EcMin*self.catalise
