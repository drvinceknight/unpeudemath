---
layout     : post
title      : "Allocating final year projects to students"
categories : math
tags       :
- allocation
- math
- education
comments   : true
---

Every year, our final year students are offered the chance to do a research
project. These are credit baring and take the place of another taught course.
Allocating students to project is not simple task as many students might want to
work on the same project for example.
In
this blog post I'll describe the mathematical model used to quantify how good an
allocation is and then show how we used Python (specifically the
[`pulp`](https://github.com/coin-or/pulp) library) to get the best possible
allocation.

In our [School](http://www.cardiff.ac.uk/mathematics) the process of allocating
project starts with all members of staff writing project descriptions which are
then circulated to students. Students are then asked to rank their top 4
projects.

---

## Problem inputs

---

Assuming we have \\(I\\) students and \\(J\\) projects, this can be translated 
mathematically to a **preference matrix**: \\(A\in\mathbb{Z}^{I\times J}\\) 
where \\(A_{ij}\\) is the rank of project \\(j\\) assigned by student \\(i\\).
If student \\(i\\) did not pick project \\(j\\) then \\(A_{ij}=0\\).

So for example the following matrix for \\(I=4\\) and \\(J=8\\) implies that the
second student's 3rd choice project would be project 7:

$$
A = 
\begin{pmatrix}
    0 & 2 & 3 & 1 & 4 & 0 & 0 & 0 \\
    1 & 2 & 0 & 0 & 0 & 4 & 0 & 3 \\
    0 & 2 & 0 & 0 & 4 & 1 & 3 & 0 \\
    0 & 4 & 0 & 3 & 0 & 0 & 1 & 2 \\
\end{pmatrix}
$$

Because of the combinatorial nature of things: not all students **can** be
guaranteed a project, however:

1. Some students **must** be given a project: in our case this corresponds to
   our Masters students.
2. When all else is equal the tie breaker between two students will be their
   year average from the previous year.

These two things can be captured mathematically by two vectors: \\(\alpha,
\omega \in\mathbb{R} ^ I\\), where \\(\alpha_i\\) is the average mark of student
\\(i\\) and:

$$
\omega_i = 
\begin{cases}
    0,&\text{ if student }i\text{ is a Bachelors student}\\
    1,&\text{ if student }i\text{ is a Masters student}
\end{cases}
$$

We will return to \\(\alpha, \omega\\) shortly but first let us consider how we
will represent a given allocation. This will be denoted by a matrix
\\(x\in\\{0, 1\\}^{I\times J}\\) where:


$$
x_{ij} = 
\begin{cases}
    1,&\text{ if student }i\text{ is allocated to project }j\\
    0,&\text{ otherwise}
\end{cases}
$$

So for example the following represents an allocation where all students would
get their first choice:

$$
x = 
\begin{pmatrix}
    0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\
    1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\
    0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\
\end{pmatrix}
$$

An important consideration when allocating students is not just the student
preference but also the workload implications on staff who supervise them:

1. Projects can only be allocated a number of times (in our School this number
   is 2). Theoretically this could differ on a project by project basis and will
   be represented by \\(\chi\in\mathbb{Z}^J\\).
2. Supervisors (who can offer multiple projects) can only take on certain number
   of students. This is usually 2 but in some cases for members of staff with
   high workloads this is 1. 
2. Supervisors (who can offer multiple projects) can only take on a certain number
   of "credits": for example Masters projects correspond to twice as many
   credits (40) as Bachelors projects (20). In general supervisors are limited
   to 40 credits (so 2 Bachelors projects or 1 Masters project).

Assuming there are \\(K\\) supervisors these upper bounds will be denoted by:

$$
\beta\in\mathbb{Z}^{K}\qquad
\kappa\in\mathbb{R}^{K}
$$

We capture the projects supervised by each member of staff using
\\(S\in\mathbb{Z}^{K\times N}\\) where \\(S_{kj}\\) is the number of credits of
project \\(j\\) if it is offered by supervisor \\(k\\) (0 if not).

Now there are a number of constraints on what is to be considered a **valid**
allocation:

---

## Problem constraints

---

### All students must be allocated to at most one project:

$$\sum_{j=1}^{J}x_{ij}\leq1\;\forall\;1\leq i\leq I$$

### There is a lower bound on the allocation of the number of students (in our case specifically for Masters students)

 $$\sum_{j=1}^{J}x_{ij}\geq \omega_i\;\forall\;1\leq i\leq I$$

### Student can only be allocated to projects they have chosen:

$$x_{ij}\leq A_{ij}\;\forall\;1\leq i\leq I,\;1\leq j\leq J$$

(Thus if \\(A_{ij}=0\\) \\(x_{ij}=0\\).)

### Every project can only be allocated to a given number of students

$$\sum_{i=1}^Ix_{ij}\leq \chi_j\;\forall\;1\leq j\leq J$$


### Every supervisor can only supervise a given number of projects

For the **number** of
students each supervisor can take on we have the constraint:

$$\sum_{j=1}^{J} \frac{S_{kj}}{\max(S_{kj}, 1)}\sum_{i=1}^{I} x_{ij}\leq
\beta_k\;\forall\;1\leq k\leq K$$

For the **number** of
credits each supervisor can take on we have the constraints:

$$\sum_{j=1}^{J}S_{kj}\sum_{i=1}^{I} x_{ij}\leq \kappa_k\;\forall\;1\leq k\leq
K$$

---

## Evaluating a solution

---

Our goal is to give as many students as possible as high a ranked project as
possible. If all things are equal we will use their marks in previous years to
give them a better chance. Note that due to the combinatorial nature of this
problem, that does not mean an individual student with a mark higher than an
other will get priority over that student. Because of the feasability
constraints and the numerous interactions this will not necessarily occur.

The objective function used is (in a maximisation framework):

$$c(x) = \sum_{i=1}^{I}\sum_{j=1}^{J}x_{ij}\frac{\alpha_{i}}{A_{ij}}$$

thus \\(\alpha_{i}/A_{ij}\\) is a scaling assigned to project \\(j\\) when
picked by student \\(i\\):

- If the project is highly ranked it (so less preferable) it contributes less;
- If the student has a high mark it contributes more.

---

## Finding the best solution

---

An important part of the objective function \\(c\\) is that it is linear in
\\(x\\) (there are no terms like \\(x_{13} ^ 2\\)). This implies that we can use
a neat mathematical tool call [Integer Linear
Programming](https://en.wikipedia.org/wiki/Integer_programming) to find a
solution to the problem of optimising \\(c(x)\\) over the constraints listed
above.

I've written about this sort of thing a few times now, if you're interested in
seeing other examples take a look at:

- [Scheduling class
  presentation](http://vknight.org/unpeudemath/mathematics/2017/03/01/Scheduling-class-presentations-using-pulp.html)
- [Scheduling the upcoming PyCon UK
  conference](http://vknight.org/unpeudemath/python/2017/05/06/scheduling-a-conference-with-linear-programming-and-python.html)
  which has lead to a Python library specifically for the scheduling of
  conferences:
  [conference-scheduler.readthedocs.io](http://conference-scheduler.readthedocs.io/en/latest/)


In this particular case, once the various inputs have been read in (in our case
we did this by reading in an excel spreadsheet) the following Python function is
all we need:

```python
def create_prob(A=A, alpha=alpha, S=S, chi=chi, beta=beta, kappa=kappa, omega=omega):

    number_of_students, number_of_projects = A.shape
    prob = pulp.LpProblem("Project matching", pulp.LpMaximize)
    x = pulp.LpVariable.dicts("x", itertools.product(range(number_of_students), range(number_of_projects)),
                              cat=pulp.LpBinary)  # Variables
    
    objective_function = 0
    for student in range(number_of_students):
        for project in range(number_of_projects):
            if A[(student, project)] > 0:
                objective_function += x[(student, project)] * (alpha[student]) / ((A[(student, project)]))
    prob += objective_function
    
    # The upper bound
    for student, project in x:
        prob += x[student, project] <= float(A[student, project])
        
    # At most chi_j student for every project
    for project in range(number_of_projects):
        prob += sum(x[(student, project)] for student in range(number_of_students)) <= chi[project]
    
    # At most 1 project per student
    for student in range(number_of_students):
        prob += sum(x[(student, project)] for project in range(number_of_projects)) <= 1
        
    # At least omega_i project per student
    for student in range(number_of_students):
        prob += sum(x[(student, project)] for project in range(number_of_projects)) >= omega[student]
        
    # Number of projects supervised
    for k, supervisor in enumerate(S):
        prob += sum(supervisor[project] / (max(1, supervisor[project])) * sum(x[(student, project)] 
                                              for student in range(number_of_students)) 
                    for project in range(number_of_projects)) <= beta[k]
        
    # Number of credits supervised
    for k, supervisor in enumerate(S):
        prob += sum(supervisor[project] * sum(x[(student, project)] 
                                              for student in range(number_of_students)) 
                    for project in range(number_of_projects)) <= kappa[k]
        
    return prob, x
```

The following then creates the problem and solves it:

```python

>>> prob, x = create_prob(A=A, alpha=alpha, S=S, beta=beta, kappa=kappa, omega=omega)
>>> prob.solve()
1
```

The return of `1` simply indicates that the solver arrived at the solution 
successfully.

### Reflections

Note that all of this can be implemented and done directly in Python which is
Open source. The one library that is needed is called `pulp` which can be
installed straightforwardly using `pip install pulp`.

The solution approach here is **exact**: it uses integer linear programming,
theoretically, as the problem becomes more complex it could take more
computational time to find a solution. In these cases heuristic algorithms such
as [simulated annealing](https://en.wikipedia.org/wiki/Simulated_annealing) or
[genetic algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm) can be
used. **However** in practice, this should scale readily for the "usual" class
size.

One of the great uses of this type of approach is that it is first of all
transparent (if students ask why they have been allocated a certain project we
can say why). Second of all, it takes no time to create a new solution given a
set of inputs. Whilst it took a bit of time this Summer to write down the
mathematical model and the Python code (most of the difficulties with the code
was actually reading in the various inputs), next year this should 
take no time at all.

Finally, the mathematical model is generic enough to be usable by
others however if there are certain constraints that are not captured these
should be (famous last words) straightforward to add.
