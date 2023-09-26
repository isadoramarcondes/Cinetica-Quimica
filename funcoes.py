import numpy as np
import random as rd
from particula import Particula

def step(particulas, step, tamanho):
    """Calcula um passo da simulação para cada partícula"""
    
    # Detect edge-hitting and collision of every particle
    for i in range(len(particulas)):
        particulas[i].calc_col_parede(step,tamanho)
        for j in range(i+1,len(particulas)):
                particulas[i].calc_col(particulas[j],step)    

                
    # Compute position of every particle  
    for particula in particulas:
        particula.update(step)
        
        
def lista_inicial(N, raio, massa, tamanho_caixa, reatividade):
    """Gerar uma lista de partículas inicial"""
    particulas = []

    for i in range(N):
        
        v_mag = np.random.rand(1)*20
        v_ang = np.random.rand(1)*2*np.pi
        v = np.append(v_mag*np.cos(v_ang), v_mag*np.sin(v_ang))
        
        colisao = True
        while(colisao == True):
            
            colisao = False
            pos = raio + np.random.rand(2)*(tamanho_caixa-2*raio) 
            nova_particula = Particula(pos, v, raio, massa, reatividade)
            for j in range(len(particulas)):

                colisao = nova_particula.checar_col(particulas[j] )

                if colisao == True:
                    break

        particulas.append(nova_particula)
    return particulas