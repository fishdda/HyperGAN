from hypergan.samplers.base_sampler import BaseSampler

import tensorflow as tf
import numpy as np

class SegmentSampler(BaseSampler):
    def __init__(self, gan):
        BaseSampler.__init__(self, gan)
        self.x_v = None
        self.z_v = None
        self.created = False
    def _sample(self):
        gan = self.gan
        x_t = gan.inputs.x
        g_t = gan.autoencoded_x
        z_t = gan.uniform_encoder.sample

        g1x_t = gan.generator.g1x
        g2x_t = gan.generator.g2x
        mask_t = None


        sess = gan.session
        config = gan.config
        if(not self.created):
            self.x_v = sess.run(x_t)
            self.created=True
            self.mask_t = (gan.generator.mask-0.5*2)

        gens = sess.run(
                [
                    gan.inputs.x,
                    mask_t,
                    g_t,
                    g1x_t,
                    g2x_t
                ], {
                    x_t: self.x_v
                })

        stacks = []
        bs = gan.batch_size() // 2
        width = min(gan.batch_size(), 8)
        for gen in gens:
            for i in range(1):
                stacks.append([gen[i*width+j] for j in range(width)])

        images = np.vstack(stacks)
        return {'generator':images}


