# Paint batch optimizer service

## Purpose

This service provides solutions for the following problem.

Our users own paint factories. There are N different colors they can mix, and each color can be prepared "matte" or "glossy". So, you can make 2N different types of paint.

Each of their customers has a set of paint types they like, and customers will be satisfied if you have at least one of those types prepared.
At most one of the types a customer likes will be a "matte".

Our user wants to make N batches of paint, so that:

There is exactly one batch for each color of paint, and it is either matte or glossy. For each customer, user makes at least one paint that they like.
The minimum possible number of batches are matte (since matte is more expensive to make). This service finds whether it is possible to satisfy all
customers given these constraints, and if it is, what paint types you should make. If it is possible to satisfy all your customers, there will be only
one answer which minimizes the number of matte batches.

Input

Integer N, the number of paint colors,  integer M, the number of customers. A list of M lists, one for each customer, each containing: An integer T >= 1,
the number of paint types the customer likes, followed by T pairs of integers "X Y", one for each type the customer likes, where X is the paint color
between 1 and N inclusive, and Y is either 0 to indicate glossy, or 1 to indicated matte. Note that: No pair will occur more than once for a single customer.
Each customer will have at least one color that they like (T >= 1). Each customer will like at most one matte color. (At most one pair for each customer has Y = 1).

Output

The string "IMPOSSIBLE", if the customers' preferences cannot be satisfied; OR N space-separated integers, one for each color from 1 to N, which are 0 if
the corresponding paint should be prepared glossy, and 1 if it should be matte.

## Usage

In the `app` directory you will see a small Python web service (`app.py`), a dependency list (`requirements.txt`) and a `Makefile`. The `Makefile` contains
2 targets: `build` that just installs the requirements into the current Python environment, and `run` which runs an example instance of the application.

The application has a primary endpoint at `/v1/`. When you make calls to this endpoint, you can send a JSON string as the argument "input". The JSON string
contains three keys: colors, costumers and demands.

Examples:

http://0.0.0.0:8080/v1/?input={%22colors%22:1,%22customers%22:2,%22demands%22:[[1,1,1],[1,1,0]]}
IMPOSSIBLE

http://0.0.0.0:8080/v1/?input={%22colors%22:5,%22customers%22:3,%22demands%22:[[1,1,1],[2,1,0,2,0],[1,5,0]]}
1 0 0 0 0

## Limitations

None of our users produce more than 2000 different colors, or have more than 2000 customers. (1 <= N <= 2000 1 <= M <= 2000)
The sum of all the T values for the customers in a request will not exceed 3000.

## Done

* Migrated to [pipenv](https://pipenv.readthedocs.io/)
* Solver: fixed glossy/mattes bug
* Solver: improved algo

## TODO

* Bump recursion limit
* Tests: Add Flask [integration tests](http://flask.pocoo.org/docs/1.0/testing/#the-application) which would be much easier to run than current setup.
* API v2: Use request body for JSON instead of GET
* API v2: More verbose "demands"

## Solver algo

Currently we're building a tree of all possible solutions, select the ones which meet all customers' needs (so check all customers)
and find the one with as few matte batches as possible (so we're computing the sum/len too).

It's O(N * N * M), worst case is 2000 * 2000 * 2000 == 8 billion iterations and quite heavy on RAM too.

How we can improve this?

I've tried other tree building approaches (tree of demands) but they're also quite complex. So let's just refactor and
add some pruning. I've also improved solution check by using bitmasks instead of manual checks.

## New solver algo

Let's save some RAM and CPU. Instead of a tree, let's iterate through the customers, and populate mattes bucket (set actually)
if it helps current customer to become satisfied (i.e. if he has matte demand, and it's not met yet, and all his glossy demands fail).
If we made any changes to the mattes bucket, re-run the iteration. If not (all customers are satisfied), return the current mattes bucket.

Worst case CPU complexity is still high: O(M * M * T) but the best case is just O(M) (everyone is satisfied straight away), and the average
is also way better: in all the test cases it's at least 3 times faster than the bit arrays solution, plus we got rid of the recursion,
so we don't need piles of RAM anymore. Space complexity is O(N + T) now, and we can improve it a bit more by preparing demands for each
customer (as you did in the original solution).

Though, if customers could demand few matte batches, we would still have to build the tree.
