##################################
#### assignment and unicode symbols 🔥🔥🔥
##################################

# silly example 
🔥 = -42
💧 = 42
🔥 + 💧

# Golden ratio (nice vs. old)
φ = (1 + √5)/2

# pi 
pi
π

# Navier stokes
∇ = randn(10)
u = randn(10)
𝒫 = 0.0
ρ = 10
# ρ * (u ⋅ (∇*u)) + 𝒫
##################################
#### Arrays/Vectors/Matrices
##################################

# defining a vector
powers_of_two = [1, 2, 4.0]
some_random_stuff = ["SWSSS2023", 3, 1.0, +]

# appending stuff/mutating vectors: push!, append!

# defining a matrix
vandermonde = [1 2 4 8;  # first row
                 1 3 9 27] # second row

# concatenating 
# adding rows 
add_a_row = [vandermonde;
            1 4 16 48]

# adding columns
add_a_col = [vandermonde vandermonde]
add_a_col2 = [vandermonde [0; 1]]

# indexing starts at 1!
add_a_col[1,1]

# slicing
add_a_col[:, 2:4]
# last element is indexed by end keyword
add_a_col[:, end]
##################################
#### loops + printing
##################################
for power in powers_of_two
    println(power)
end

push!(powers_of_two, 8)

append!(powers_of_two, [16, 32])

i = 0
while i < 10
    println(i)
    i += 1
end

#in particular ranges are written with : instead of range function
#range(5) in python <=> 0:4 in julia 
range = 0:4

##################################
#### if-elseif-else 
##################################
a = 5.0

if a < 2.5
    println("a is less than 2.5")
elseif a < 3.5
    println("a is less than 3.5")
else
    println("a is not less than 3.5")
end

##################################
#### functions
##################################

# functional programming style
function my_add(a, b)
    c = a + b
    return c
end

Σ = my_add(5, 3)

function my_add(a::Float64, b::Int)
    
    return a
end
Σ = my_add(5.0, 3)

# for simple functions we may prefer the assignment form 
# to resemble standard math notation more closely
f(x) = 1/(2π)*exp(-1/2*x^2)

# evaluation 
p = f(0.5)

# vectorization/(map-reduce)
# evaluates our function at every element of the supplied 
# vector/array and returns the result in the same shape!
f.([1.0, 2.0, 0.5, 0.7])

# differences between python and julia
# Why Julia was created
# https://julialang.org/blog/2012/02/why-we-created-julia/# 
# Julia documentation: Noteworthy differences to other common languages
# https://docs.julialang.org/en/v1/manual/noteworthy-differences/
# Julia for data science
# https://www.imaginarycloud.com/blog/julia-vs-python/#future