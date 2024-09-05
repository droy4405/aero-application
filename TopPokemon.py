import pandas as pd
import numpy as np
import os
import cv2


class TopPokemon:

    def __init__(self, path):
        self.path = path

    def redPixels(self, image):
        try:
            # Read the image
            img = cv2.imread(image)
            if img is None:
                raise ValueError(f"Image not found: {image}")

            # Convert the image to HSV color space
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Define the lower and upper bounds for red pixels in HSV color space
            lower_red1 = np.array([0, 100, 20])
            upper_red1 = np.array([10, 255, 255])

            lower_red2 = np.array([160, 100, 20])
            upper_red2 = np.array([179, 255, 255])

            # Create two masks for red pixels in both ranges
            mask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)

            red_mask = mask1 + mask2

            # Count the red pixels
            red_pixel_count = np.count_nonzero(red_mask)

            return red_pixel_count

        except Exception as e:
            print(f"Error processing image {image}: {e}")
            return 0  # Return 0 red pixels in case of an error

    def redAttack(self):
        try:
            # List all image files in the directory
            dir_list = os.listdir(self.path)
            df = pd.read_csv('processed_names_and_attack.csv')

            # Dictionary to store red pixel counts
            redPixelsDict = {}

            # Sort image files using custom key
            for image in sorted(dir_list, key=custom_sort_key):
                redPixelsDict.update({image: self.redPixels(self.path + '/' + image)})

            # Sort DataFrame by name (ensure it's sorted the same way as images)
            df.sort_values(["name"], axis=0, ascending=[True], inplace=True)

            # Convert the DataFrame into a list of dictionaries
            data_dict = df.to_dict(orient='records')

            attack = []
            redAttackDict = {}

            # Extract attack values from the DataFrame
            for pokemon in data_dict:
                attack.append(pokemon.get("attack", 0))  # Default to 0 if attack is missing

            # Multiply red pixel count with attack value
            i = 0
            for key in redPixelsDict:
                if i < len(attack):
                    redAttackDict.update({key: redPixelsDict[key] * float(attack[i])})
                i += 1

            top_three = sorted(redAttackDict.items(), key=lambda x: x[1], reverse=True)[:3]

            # Return the result as a dictionary with the top three keys and values
            return dict(top_three)

        except Exception as e:
            print(f"Error in redAttack computation: {e}")
            return {}


# Custom sorting function to handle file names
def custom_sort_key(s):
    return s.replace('-', 'zzz')


# Example usage
if __name__ == "__main__":
    print(TopPokemon('/home/droy/aero-pokemon-data/data').redAttack())
