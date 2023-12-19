import gurobipy as gp
from gurobipy import GRB
import numpy as np

# Function to read input from a text file
def read_input_file(filename):

    with open(filename, 'r') as file:
        # The first line contains five integers each representing the following values:
        # n: Total Data-items (in all the clusters)
        # K: Number of Cluster
        # N: Number of Tags
        # alpha: max size of descriptor for each cluster
        # beta: max overlap between two descriptors
        n, K, N, alpha, beta = map(int, file.readline().strip().split())
        # Read tag categories from the second line
        tag_cats = list(map(int, file.readline().strip().split()))


        B = []
        clusters = []

        for _ in range(n):
            data_item, cluster, *tags = map(int, file.readline().strip().split())
            B.append(tags) # tag set for each data-item will have 0 or 1 values
            clusters.append(cluster) # Cluster number for each data-item

        return n, K, N, alpha, beta, tag_cats, B, clusters

# Define the problem
model = gp.Model("ClusterDescriptors")

# Read input from a text file
n, K, N,alpha,beta,tag_cats,B,clusters = read_input_file("tagged_data_test_2_c3.txt")
print("n:",n)
print("K:",K)
print("N:",N)
print("alpha:",alpha)
print("beta:",beta)
# print(tag_cats)
# print("B:",B)
#print("clusters:",clusters)

# Creating M array
M = np.zeros((n, K), dtype=int)

for i, k in enumerate(clusters):
    M[i,k] = 1
    
# Defining the variables
y = {}
w = {}

# Adding variables
# y_j,k: tag j in descriptor for cluster k

for j in range(1,N+1):
    for k in range(1,K+1):
        y[j, k] = model.addVar(vtype=GRB.BINARY, name=f"y_{j}_{k}")

# w_i: data-point i is covered by its cluster descriptor
for i in range(1, n+1):
    w[i] = model.addVar(vtype=GRB.BINARY, name=f"w_{i}")

# Update the model to include new variables
model.update()

# Adding  constraints

# # Constraint a
# for i in range(1,n+1): # Iterating through the data-items
# # B[i-1][j-1] tells us if data-item i uses tag j
# # y[j,clusters[i-1]] tells us if tag j is in the descriptor k (descriptor of the data-item's cluster)
# # Overall ensures that there is atleast one tag pertaining to each data-item in the cluster in its decriptor


#     # output_file.write(str(gp.quicksum(B[i-1][j-1] * y[j, clusters[i-1]] for j in range(1,N + 1)) >= 1))
#     # output_file.write("\n\n")
#     model.addConstr(gp.quicksum(B[i-1][j-1] * y[j, clusters[i-1]+1] for j in range(1,N + 1)) >= 1)


# Constraint b
# Overall ensures that the size of each descriptor is at most alpha
for k in range(1,K+1): #Iterating through the descriptors
# Specifying that the sum of all the tags for a given descriptor i.e., is less that alpha

    # output_file.write(str(gp.quicksum(y[j, k] for j in range(1,N+1)) <= alpha))
    # output_file.write("\n\n")

    model.addConstr(gp.quicksum(y[j, k] for j in range(1,N+1)) <= alpha)

# Constraint c
# y_j,k tells us if tag j is in descriptor k and y_j,l tells us if tag j is in descriptor l
## y_j,k * y_j,l tells us how many data-items are in both descriptor k and l since it will only add 1 to the sum when both y_j,k and y_j,l are 1
# Overall ensures that the overlap between any pair of descriptors is at most beta
# We check this for all pairs of descriptors
for k in range(1,K+1):

    for l in range(k+1, K+1):
        # output_file.write(str(gp.quicksum(y[j, k] * y[j, l] for j in range(1,N+1))<= beta))
        model.addConstr(gp.quicksum(y[j, k] * y[j, l] for j in range(1,N+1)) <= beta)

# Constraint d
# Ensures each cluster cannot have all tags of the same type
for k in range(1, K + 1):

    for t in set(tag_cats):
        # Ensure that not all tags of the same type are in the descriptor
        len_tag_cat = tag_cats.count(t)
        model.addConstr(gp.quicksum(y[j, k] for j in range(1, N + 1) if tag_cats[j - 1] == t) <= len_tag_cat - 1)

# Constraint y_j,k is binary accounted for during variable declaration

# Cover-or-Forget
        
# Constraint 1
for i in range(1, n+1):
    model.addConstr(gp.quicksum(B[i-1][j-1] * y[j, clusters[i-1]+1] for j in range(1,N + 1)) >= w[i])


# Constraint 2
for i in range(1, n+1):
    for j in range(1, N+1):
        model.addConstr(w[i] >= B[i-1][j-1] * y[j, clusters[i-1]+1])

# Constraint 3
for k in range(1,K+1):
    nk = sum(1 for i in range(1, n + 1) if clusters[i - 1]+1 == k)
    delta = 0.9

    model.addConstr(gp.quicksum(M[i-1,k-1] * w[i] for i in range(1, n+1)) >= np.ceil(delta * nk))


# Constraint e

# for j in range(1, N + 1):
#     for k in range(1, K + 1):
#         # y[j, k] is in the descriptor of cluster k
#         # Ensures that if y[j, k] is 1 (tag is in descriptor), then at least one data-item in the cluster has the tag
#         model.addConstr(gp.quicksum(B[i-1][j-1] for i in range(1, n+1) if clusters[i-1] == k) >= y[j, k])


# Objective function to minimize the sum of y_j,k
model.setObjective(gp.quicksum(y[j, k] for j in range(1, N+1) for k in range(1, K+1)), GRB.MINIMIZE)

# Solve the model
model.optimize()

# # Open a file for writing the results
# with open("results_c5.txt", "a") as output_file:
#     output_file.write(f"alpha:{alpha} ")
#     output_file.write(f"beta: {beta} ")

if model.status == GRB.OPTIMAL:
        for k in range(1, K + 1):
            cluster_tags = [j for j in range(1, N + 1) if y[j, k].x == 1.0]
            print(f"\nCluster {k-1} Descriptor:")
            print(f"Tags: {cluster_tags}")

            # for i in range(1, n + 1): # Print corresponding data items and their tags
            #     if clusters[i - 1] == k:
            #         data_item_tags = [j for j in range(1, N + 1) if B[i - 1][j - 1] == 1]
            #         print(f"Data Item {i} Tags:", data_item_tags)

            # for j in range(1, N + 1):
            #     print(f"{y[j, k].varName}: {y[j, k].x}\n")
else:
    print("No solution found.\n")

model.dispose()

#    	num_solutions = model.getAttr(GRB.Attr.SolCount)
#    	print(f"Number of solutions in the pool: {num_solutions}")
    # for k in range(1, K + 1):
    #        for j in range(1, N + 1):
    #            output_file.write(f"{y[j, k].varName}: {y[j, k].x}\n")
