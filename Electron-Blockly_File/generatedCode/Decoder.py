class Decoder(nn.Module):
  #
  latent_dim : int
  @nn.compact
  def __call__(self, z):
      #
      z = nn.Dense(features=7*7*64)(z)

      z = z.reshape(z.shape[0], 7, 7, 64)

      z = nn.ConvTranspose(features=32, kernel_size=(3, 3), strides=(2, 2), padding="SAME")(z)

      z = nn.relu(z)

      z = nn.ConvTranspose(features=1, kernel_size=(3, 3), strides=(2, 2), padding="SAME")(z)

      z = nn.sigmoid(z)

      return z
