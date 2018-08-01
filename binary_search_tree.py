class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        
    def hasLeftChild(self):
        return bool(self.leftChild)
    
    def hasRightChild(self):
        return bool(self.rightChild)
    
    def isLeftChild(self):
        if (not self.isRoot()) and self.parent.leftChild == self:
            return True
        return False
    
    def isRightChild(self):
        if (not self.isRoot()) and self.parent.rightChild == self:
            return True
        return False
    
    def isRoot(self):
        return not bool(self.parent)
    
    def isLeaf(self):
        return not (self.hasLeftChild() or self.hasRightChild())
    
    def hasAnyChildren(self):
        return not self.isLeaf()
    
    def hasBothChildren(self):
        return (self.hasLeftChild() and self.hasRightChild())
    
    def replaceNodeData(self, key, value, lc, rc):
        self.key, self.payload, self.leftChild, self.rightChild = key, value, lc, rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self
    
    def print_all(self):
        print(self.key, self.payload, 
              self.leftChild.key if self.hasLeftChild() else 'X',
              self.rightChild.key if self.hasRightChild() else 'X')
        if self.hasLeftChild():
            self.leftChild.print_all()
        if self.hasRightChild():
            self.rightChild.print_all()

            
    def __iter__(self):
        if self:
            if self.hasLeftChild():
                for elem in self.leftChild:
                    yield elem
            yield self.key
            if self.hasRightChild():
                for elem in self.rightChild:
                    yield elem
                    
    def findSuccessor(self):
        return self.rightChild.findMin()
    
    def findMin(self):
        current = self
        
        while current.hasLeftChild():
            current = current.leftChild
        
        return current
    
    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else:
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent
                    
class BinarySearchTree:
    
    def __init__(self):
        self.root = None
        self.size = 0
        
    def length(self):
        return self.size
    
    def __len__(self): # for len(treeobj)
        return self.size
    
    def __iter__(self): # for node in treeobj: # do something
        return self.root.__iter__()
    
    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size += 1
        
    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent = currentNode)
        elif key > currentNode.key:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent = currentNode)
    
    def __setitem__(self, k, v):
        self.put(k, v)
        
    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None
        
    def _get(self, key, currentNode):
        if currentNode.key == key:
            return currentNode
        elif currentNode.key > key:
            return self._get(key, currentNode.leftChild)
        elif currentNode.key < key:
            return self._get(key, currentNode.rightChild)
        else:
            return None
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __contains__(self, key):
        if self.get(key):
            return True
        return False
    
    def delete(self, key):
        if self.size > 1:
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size -= 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('Error, key not in tree')
        
    def __delitem__(self, key): # enabling del tree[key]
        self.delete(key)
        
    def remove(self, currentNode):
        if currentNode.isLeaf():
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren():
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.payload = succ.payload
        else:
            if currentNode.hasLeftChild():
                currentNode.leftChild.parent = currentNode.parent
                if currentNode.isLeftChild():
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.parent.rightChild = currentNode.leftChild
                else: 
                    # currentNode = currentNode.leftChild
                    currentNode.replaceNodeData(currentNode.leftChild.key, currentNode.leftChild.payload, \
                            currentNode.leftChild.leftChild, currentNode.leftChild.rightChild)
            else:
                currentNode.rightChild.parent = currentNode.parent
                if currentNode.isLeftChild():
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    # currentNode = currentNode.rightChild
                    currentNode.replaceNodeData(currentNode.rightChild.key, currentNode.rightChild.payload, \
                            currentNode.rightChild.leftChild, currentNode.rightChild.rightChild)
                    
            
                
    def to_list(self):
        if self.root:
            return [(key, self[key]) for key in self]
        else:
            return []
    
    def __str__(self):
        return str(self.to_list())
    
'''
import random as rd

def test():
    for i in range(30):
        n = rd.randint(1, 10)
        nodes = rd.sample(range(0, 100), n)
        bst = BinarySearchTree()
        
        for node in nodes:
            bst[node] = node
        print('-'*50)
        print(nodes)
        print("K C L R")
        bst.root.print_all()
        delNodes= rd.sample(nodes, rd.randint(1, n))
        rd.shuffle(delNodes)
        print(delNodes)
        print()
        
        for delNode in delNodes:
            print('current length:', len(bst))
            print('deleting', delNode)
            bst.delete(delNode)
            print("K C L R")
            if bst.root:
                bst.root.print_all()
            else:
                print('All deleted')
            print()

        if bst.root:
            print("K C L R")
            bst.root.print_all()
        print()
'''

def main():    
    nodes = [17, 5, 25, 2, 11, 29, 38, 9, 16, 7, 8]
    bst = BinarySearchTree()
    
    
    
    for node in nodes:
        bst[node] = node
           
    print('K C L R')
    bst.root.print_all()
    bst.delete(29)
    
if __name__ == '__main__':
    main()