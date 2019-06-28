public class balancedBinaryTree {
    /**
     * @param root: The root of binary tree.
     * @return: True if this Binary tree is Balanced, or false.
     */
    public boolean isBalanced(TreeNode root) {
        // write your code here
        return helper(root, 0).isBalanced;
    }
 
    // This is not needed. Can just check the depth
    private class Result {
        boolean isBalanced;
        int height;
        Result(boolean isBalanced, int height) {
            this.isBalanced = isBalanced;
            this.height = height;
        }
    }
    private Result helper(TreeNode root, int depth) {
        if (root == null) {
            return new Result(true, depth);
        }
        Result left = helper(root.left, depth + 1);
        Result right = helper(root.right, depth + 1);
 
        if (!left.isBalanced || !right.isBalanced) {
            return new Result(false, 0);
        }
 
        if (Math.abs(left.height - right.height) > 1) {
            return new Result(false, 0);
        }
        return new Result(true, Math.max(left.height, right.height));
    }
    
}