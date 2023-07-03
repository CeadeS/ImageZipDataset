import os
import torch
from PIL import Image
import pandas as pd
from zipfile import ZipFile
import logging
import random

class ImageZipDataset(torch.utils.data.Dataset):
    def __init__(self, zip_path, info_path, transform=None, target_transform=None, delimiter='\t',
                split='train', n_crossval_split=-1, n_crossval=None, eval_proportion = .2, random_seed=3):
        if not n_crossval is None:
            assert isinstance(n_crossval_split, int)
            assert n_crossval_split in range(n_crossval)
        assert split in ['train', 'val']
        assert isinstance(eval_proportion, float)

        
            
        self._zip_path = zip_path
        self.transform = transform
        self.target_transform = target_transform
        self.zip_file = None                    
        
        self.metadata = pd.read_csv(info_path,delimiter=delimiter)
        
        # prepare deterministic random index order
        self.indices = list(range(len(self.metadata)))
        random.Random(random_seed).shuffle(self.indices)
        # prepare split
        
        if isinstance(n_crossval, int): 
            if n_crossval_split == -1:
                n_crossval_split == random.randint(0,n_crossval)
            l = len(self.indices)//n_crossval
            logging.info(f"Initializing the {n_crossval_split}th - {n_crossval}-fold crossvalidation {split}-split")
            if  split != 'train':
                self.indices = self.indices[int(n_crossval_split*l):int((n_crossval_split+1)*l)]                
            else:
                self.indices = self.indices[:int(n_crossval_split*l)]+self.indices[int((n_crossval_split+1)*l):]   
        else:
            l = len(self.indices)            
            if  split == 'train':
                logging.info(f"Initializing the {(1-eval_proportion)*100:.0f}% {split} split")
                self.indices = self.indices[:int((1-eval_proportion)*l)]                
            else:
                logging.info(f"Initializing the {(eval_proportion)*100:.0f}% {split} split")
                self.indices = self.indices[int((1-eval_proportion)*l):]
            
            
        self.classes = self.metadata.label.unique()
        print(f"number classes {len(self.classes)}")
        
        self.samples = list(zip(self.metadata['fileName'], self.metadata['label']))

    def __getitem__(self, index):
        """
        Args:
            index (int): Index
        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        """
        #resolve index
        index = self.indices[index]
        if self.zip_file is None:
            self.zip_file = ZipFile(self._zip_path, 'r')
            
        path, target = self.samples[index]
        target = torch.as_tensor(target)

        with self.zip_file.open(path) as f:
            sample = Image.open(f).convert('RGB')

        if self.transform is not None:
            sample = self.transform(sample)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return sample, target

    def __len__(self):
        return len(self.indices)

    def __repr__(self):
        fmt_str = 'Dataset ' + self.__class__.__name__ + '\n'
        fmt_str += '    Number of datapoints: {}\n'.format(self.__len__())
        tmp = '    Transforms (if any): '
        fmt_str += '{0}{1}\n'.format(tmp, self.transform.__repr__().replace('\n', '\n' + ' ' * len(tmp)))
        tmp = '    Target Transforms (if any): '
        fmt_str += '{0}{1}'.format(tmp, self.target_transform.__repr__().replace('\n', '\n' + ' ' * len(tmp)))
        return fmt_str