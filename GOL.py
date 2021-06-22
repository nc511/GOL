from pydoc import describe
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns  
from tqdm import trange
import imageio
import os

def get_range(index, max_index):
    if index == max_index: 
        index_range = range(-1, 1, 1)
    elif index == 0:
        index_range = range(0, 2, 1)
    else:
        index_range = range(-1, 2, 1)
    return index_range
def get_neighbouring_indices(row, col, max_row, max_col):
    row_range = get_range(row, max_row)
    col_range = get_range(col, max_col)
    
    neighbours =[(row + i, col + j) for i in row_range for j in col_range]
    neighbours.remove((row, col))
    return neighbours


def get_num_neighbours(game_map, index_list):
    return sum([game_map[i] for i in index_list])  



def get_new_cell_value(row, column, game_map, max_row, max_col):
    
    neighbouring_indices = get_neighbouring_indices(row, column, max_row, max_col)
    num_neighbours = get_num_neighbours(game_map, neighbouring_indices)
    if num_neighbours == 3: 
        return 1
    is_alive = bool(game_map[row, column])

    if is_alive and num_neighbours == 2: 
        return 1
    else: 
        return 0 
    
            
    
def update_map(game_map):
    max_row = game_map.shape[0] - 1
    max_col = game_map.shape[1] - 1
    new_map = game_map.copy()
    for row in range(game_map.shape[0]):
        for column in range(game_map.shape[1]):
            new_cell_value = get_new_cell_value(row, column, game_map, max_row, max_col)
            new_map[row, column] = new_cell_value
            
    return new_map



def play_game(start_map, num_rounds):
    current_map = start_map
    for i in trange(num_rounds, desc="Playing game..."):
        plt.figure(figsize=(5,5))
        sns.heatmap(current_map, cbar=False, linewidths=0.2, linecolor="white", xticklabels=False, yticklabels=False) 
        plt.savefig(f"Round {i}.png")
        plt.close()
        current_map = update_map(current_map)

def save_gif(filename, num_rounds):
    with imageio.get_writer(filename, mode="I") as writer: 
        for i in trange(num_rounds, desc="Making gif..."): 
            round_file = f"Round {i}.png"
            image = imageio.imread(round_file)
            writer.append_data(image)
            
    for i in trange(100, desc="Removing files..."):
        os.remove(f"Round {i}.png")

def main():
    game_map = np.random.randint(0,2,(25,25))
    play_game(game_map, 100)
    save_gif("GOL.gif", 100)


if __name__ == "__main__":
    main()
