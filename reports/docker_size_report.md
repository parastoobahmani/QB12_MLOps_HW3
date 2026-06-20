# HW03 Docker Image Size Report

| Repository           | Tag       | Size   |
|:---------------------|:----------|:-------|
| qbc12-airbnb-serving | optimized | 1.29GB |
| qbc12-airbnb-serving | naive     | 3.13GB |

## Analysis
<!-- TODO: Write 2-3 sentences explaining why the sizes differ and which you would use in production. -->
I prefer to use the optimized image  since it is significantly smaller than the naive image. It uses a slimmer base image and 
    avoids copying unnecessary files into the container. A smaller image reduces storage requirements, speeds up image downloads, and improves deployment times.
    For production use, I would choose the optimized image because it is more efficient, faster to deploy, and generally has a smaller attack surface.
