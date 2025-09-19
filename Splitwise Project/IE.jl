using JuMP
using Cbc
using NamedArrays

# Define the transaction matrix
T = [0 0 0 0 0 0 0 0 0;15 0 15 15 15 15 15 15 15;0 0 0 0 0 0 0 0 0;0 0 0 0 0 30 0 0 0;0 0 0 7 0 7 7 7 7;30 60 60 55 25 0 25 0 30;0 0 0 153 153 221 0 196 146;0 0 0 0 0 0 0 0 0; 0 0 0 0 0 20 0 0 0]

# Define names directly
names = ["Anushka", "Priyanshi", "Anushka's Sis", "Tanvi", "Adarsh", "Anuttar", "Rocho", "Devesh", "Shri"]

n = length(names)

# Create and solve the optimization model
m = Model(Cbc.Optimizer)

@variable(m, s[1:n, 1:n] >= 0)
@variable(m, indicator[1:n, 1:n], Bin)

@expression(m, rowsums[i in 1:n], sum(s[i,j] for j in 1:n))
@expression(m, colsums[i in 1:n], sum(s[j,i] for j in 1:n))

@constraint(m, rowsumc[i in 1:n], (colsums[i] - rowsums[i]) == (sum(T[j,i] for j in 1:n) - sum(T[i,j] for j in 1:n)))

@constraint(m, s .<= indicator * 10000)

@objective(m, Min, sum(indicator))

optimize!(m)

I = value.(indicator)
final_transactions = value.(s)

# Print results in a readable format
println("\nMinimum transactions required: ", sum(I))

println("\nFinal transactions:")
for i in 1:n
    for j in 1:n
        if final_transactions[i, j] > 0
            println("$(names[j]) pays $(final_transactions[i, j]) to $(names[i])")
        end
    end
end
