import numpy as np

class Particula:
    
    def __init__(self, pos, velocidade, raio, massa):
        """inicializar o objeto partícula
        
        Args:
        posição da partícula
        velocidade da particula
        raio da particula
        massa da particula
        """
        self.massa = massa
        self.raio = raio
        
        # estado atual da partícula
        self.pos = np.array(pos)
        self.velocidade = np.array(velocidade)
        
        # estado gravado ao longo de toda a simulação
        self.trapos = [np.copy(self.pos)]
        self.travel = [np.copy(self.velocidade)]
        self.travel_mag = [np.linalg.norm(np.copy(self.velocidade))]
        
    def update(self, step):
        """Calcula a posição seguinte com base na velocidade"""
        self.pos += step * self.velocidade
        self.trapos.append(np.copy(self.pos)) 
        self.travel.append(np.copy(self.velocidade)) 
        self.travel_mag.append(np.linalg.norm(np.copy(self.velocidade))) 
        
    def checar_col(self, particula):
        """Checa se houve colisão com alguma partícula"""
        
        r1, r2 = self.raio, particula.raio
        x1, x2 = self.pos, particula.pos
        di = x2-x1
        norm = np.linalg.norm(di)
        if norm-(r1+r2)*1.1 < 0:
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
        if norm-(r1+r2)*1.1 < step*abs(np.dot(v1-v2, di))/norm:
            self.velocidade = v1 - 2. * m2/(m1+m2) * np.dot(v1-v2, di) / (np.linalg.norm(di)**2.) * di
            particula.velocidade = v2 - 2. * m1/(m2+m1) * np.dot(v2-v1, (-di)) / (np.linalg.norm(di)**2.) * (-di)
            

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