import jax
import jax.numpy as jnp
from flax import linen as nn
import optax
from flax.training import train_state
from jax import random
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
from torch.utils.data import DataLoader





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




class Autoencoder(nn.Module):
    latent_dim: int  # The size of the latent vector

    def setup(self):
        self.encoder = Encoder(latent_dim=self.latent_dim)
        self.decoder = Decoder(latent_dim=self.latent_dim)

    def __call__(self, x):
        # Pass the input through the encoder and then the decoder
        latent = self.encoder(x)  # Encode to latent vector
        reconstruction = self.decoder(latent)  # Decode back to the original shape
        return reconstruction

# Utility functions for model training and testin

# Define training state utility
def create_train_state(rng, learning_rate, latent_dim, input_shape):
    model = Autoencoder(latent_dim=latent_dim)
    params = model.init(rng, jnp.ones(input_shape))["params"]
    tx = optax.adam(learning_rate)
    return train_state.TrainState.create(apply_fn=model.apply, params=params, tx=tx)

def compute_loss(pred, target):
    x = jax.nn.initializers.kaiming_normal(5)
    loss = jnp.mean((pred - target) ** 2)
    jnp.mean((pred - target) ** 2)
    return loss

@jax.jit
def train_step(state, batch):
    # Compute gradients using the loss function.
    grads, _ = jax.grad(loss_fn, has_aux=True)(state.params, state.apply_fn, batch)
    return state.apply_gradients(grads=grads)

def loss_fn(params, apply_fn, batch):
    pred = apply_fn({"params": params}, batch)
    loss = compute_loss(pred, batch)
    return loss, pred


@jax.jit

def eval_step(state, batch):
    #
    return state.apply_fn({"params": state.params}, batch)



def load_data():
    transform = transforms.Compose([transforms.ToTensor()])
    train_dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
    test_dataset = datasets.MNIST(root='./data', train=False, transform=transform, download=True)

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)
    return train_loader, test_loader

train_loader, test_loader = load_data()


def train_autoencoder(latent_dim=64, num_epochs=1, learning_rate=1e-3):
    rng = random.PRNGKey(0)
    state = create_train_state(rng, learning_rate, latent_dim, (1, 28, 28, 1))  # Input shape for MNIST

    for epoch in range(num_epochs):
        for batch in train_loader:
            images, _ = batch
            images = jnp.array(images.numpy())
            images = images.reshape(-1, 28, 28, 1)

            # Training step
            state = train_step(state, images)

        print(f'Epoch {epoch+1}/{num_epochs} completed.')

    return statex

# Train the model
state = train_autoencoder()

# Evaluation and visualization
def show_images(original, reconstructed):
    fig, axes = plt.subplots(1, 2)
    axes[0].imshow(original.squeeze(), cmap='gray')
    axes[0].set_title('Original')
    axes[1].imshow(reconstructed.squeeze(), cmap='gray')
    axes[1].set_title('Reconstructed')
    plt.show()

def evaluate_autoencoder(state):
    for batch in test_loader:
        images, _ = batch
        images = jnp.array(images.numpy())
        images = images.reshape(-1, 28, 28, 1)

        # Evaluate the model on test data
        reconstructed_images = eval_step(state, images)

        # Show the first image and its reconstruction
        show_images(images[0], reconstructed_images[0])
        break

evaluate_autoencoder(state)
