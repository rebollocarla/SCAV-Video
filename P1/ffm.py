import numpy as np
import scipy.fftpack

class DCTConverter:
    def __init__(self, block_size=8):
        self.block_size = block_size

    def _dct(self, data):
        return scipy.fftpack.dct(data, type=2, norm='ortho')

    def _idct(self, data):
        return scipy.fftpack.idct(data, type=2, norm='ortho')

    def convert_to_dct(self, data):
        # Break the data into non-overlapping blocks of size block_size x block_size
        blocks = [data[i:i + self.block_size, j:j + self.block_size]
                  for i in range(0, data.shape[0], self.block_size)
                  for j in range(0, data.shape[1], self.block_size)]

        dct_blocks = []
        for block in blocks:
            dct_block = self._dct(block)
            dct_blocks.append(dct_block)

        return np.array(dct_blocks)

    def decode_dct(self, dct_data):
        # Apply inverse DCT to each block
        idct_blocks = [self._idct(dct_block) for dct_block in dct_data]

        # Reconstruct the original data by arranging the blocks
        rows = int(np.ceil(np.sqrt(len(idct_blocks))))
        cols = int(np.ceil(len(idct_blocks) / rows))
        reconstructed_data = np.zeros((rows * self.block_size, cols * self.block_size))

        for i, idct_block in enumerate(idct_blocks):
            row = i // cols
            col = i % cols
            reconstructed_data[row * self.block_size:(row + 1) * self.block_size,
                              col * self.block_size:(col + 1) * self.block_size] = idct_block

        return reconstructed_data

# Example usage:
if __name__ == "__main__":
    # Generate a random image-like data for demonstration
    image_data = np.random.randint(0, 256, size=(64, 64), dtype=np.uint8)

    dct_converter = DCTConverter()
    dct_data = dct_converter.convert_to_dct(image_data)
    decoded_data = dct_converter.decode_dct(dct_data)

    # Compare the original data and the decoded data (should be very close)
    print("Original Data:")
    print(image_data)

    print("\nDecoded Data:")
    print(decoded_data.astype(np.uint8))
