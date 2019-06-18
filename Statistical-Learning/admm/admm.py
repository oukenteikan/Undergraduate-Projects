import numpy as np
from numpy.linalg import inv, norm

class ADMM():
	def __init__(self, X, Y, rho = 1.0):
		#N for data num, p fo data dimension.
		self.N, self.p = X.shape
		self.A = X
		self.b = Y
		self.rho = rho
		#We calculate ATb and inv_ATA_rhoI here to save time,
		#otherelse we have to calculate them for every lamba.
		self.ATb = self.A.T.dot(self.b)/self.N
		self.inv_ATA_rhoI = inv(self.A.T.dot(self.A)/self.N + self.rho * np.identity(self.p))

	def objective(self):
		#The objective of lasso.
		return (1.0/2*self.N)*norm(self.A.dot(self.x)-self.b)**2 + self.lamba*norm(self.x, 1)

	def update(self):
		#Update x, z, u for each step.
		#The iterative formula derives from the derivative of augmented Lagrangian expression.
		self.x = self.inv_ATA_rhoI.dot(self.ATb + self.rho * self.z - self.u)
		t1 = self.u / self.rho + self.x
		t2 = self.lamba / self.rho
		self.z = np.maximum(t1-t2, 0) - np.maximum(0, -t1-t2)
		self.u += self.rho * (self.x - self.z)

	def solve(self, lamba = 1, maxiter = 5000, abstol = 1e-5, reltol = 1e-5):
		self.x = self.ATb.copy()
		self.z = self.x.copy()
		self.u = np.zeros(self.p)
		self.lamba = lamba
		print '%3s\t%10s\t%10s\t%10s\t%10s\t%10s' % ('iter', 'r norm', 'eps pri',
								's norm', 'eps dual', 'objective')
		iterate = 0
		history = {}
		while (True):
			iterate += 1
			zold = self.z
			self.update()
			history['objval'] = self.objective()
			history['r_norm'] = norm(self.x - self.z)
			history['s_norm'] = norm(self.rho * (self.z - zold))
			history['eps_pri'] = np.sqrt(self.p)*abstol + reltol*np.maximum(norm(self.x), norm(self.z))
			history['eps_dual'] = np.sqrt(self.N)*abstol + reltol*norm(self.rho * self.u)
			if iterate % 1000 == 0:
				print '%4d\t%10.7f\t%10.7f\t%10.7f\t%10.7f\t%10.7f' % (iterate,
					history['r_norm'], history['eps_pri'], history['s_norm'],
					history['eps_dual'], history['objval'])
			if history['r_norm'] < history['eps_pri'] and \
			history['s_norm'] < history['eps_dual'] and iterate >= maxiter:
				break

