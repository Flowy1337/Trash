class Encoder(nn.Module):
  #
  latent_dim : int
  @nn.compact
  def __call__(self, x):
      #
      x = nn.Conv(features=32, kernel_size=(3, 3), strides=(2, 2), padding="SAME")(x)

      x = nn.relu(x)

      x = nn.Conv(features=64, kernel_size=(3, 3), strides=(2, 2), padding="SAME")(x)

      x = nn.relu(x)

      x = x.reshape(x.shape[0], -1)

      x = nn.Dense(features=self.latent_dim)(x)

      return x
