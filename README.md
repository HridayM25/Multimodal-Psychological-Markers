# Multimodal-Psychological-Markers

Basic Implementation Start : Take a video, use any compression tool.

## Step 1 : Collect Models 
1) opensmile (audio)
2) vggish (audio deep) ---> Just go with this, make it trimodal
~~3) text~~
4) OpenPose (pose detection)
~~5) Face Detection (face analysis)~~
6) Optical Flow for Videos


## Step 2 : Collect Datasets 

~~1) Text is done from kaggle~~
Need to look at this.

### Fusions to Look at : 
1) Low Rank Fusion
2) Gated Fusion (Attention)
3) High Order Polynomial Fusion 

## Step 3 : Look at Early Fusion 

Concatenate all embeddings (Can look into weighted, nothing to suggest otherwise)

## Step 4 : Look at Late Fusion 

Probability Vector to Dempster-Shafer Algorithm.

## Step 5 : 

Take an element wise multiplication, then stacking for the final step
