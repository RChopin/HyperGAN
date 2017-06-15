from hypergan.samplers.base_sampler import BaseSampler

import tensorflow as tf
import numpy as np

class BeganSampler(BaseSampler):
    def __init__(self, gan):
        BaseSampler.__init__(self, gan)
        self.x_v = None
        self.z_v = None

    def sample(self, path, save_samples=False):
        gan = self.gan
        x_t = gan.inputs.x
        g_t = gan.generator.sample
        z_t = gan.encoder.sample
        
        rx_t = gan.discriminator.reconstruction

        sess = gan.session
        config = gan.config
        if(self.x_v == None):
            self.x_v, self.z_v = sess.run([x_t, z_t])

        rx_v, g_v = sess.run([rx_t, g_t], {x_t: self.x_v, z_t: self.z_v})
        stacks = []
        bs = gan.batch_size() // 2
        width = 8
        for i in range(1):
            stacks.append([self.x_v[i*width+width+j] for j in range(width)])
        for i in range(1):
            stacks.append([rx_v[i*width+width+j] for j in range(width)])
        for i in range(1):
            stacks.append([g_v[i*width+width+j] for j in range(width)])

        #[print(np.shape(s)) for s in stacks]
        images = np.vstack([np.hstack(s) for s in stacks])

        self.plot(images, path, save_samples)
        return [{'images': images, 'label': 'tiled x sample'}]
