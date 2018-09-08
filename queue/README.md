Originally, I thought Jobs were a good abstraction for WebConsoles. After experimenting a bit, I think I was wrong.

Following the "Fine Parallel Processing Using a Work Queue" example from the official [docs](https://kubernetes.io/docs/tasks/job/fine-parallel-processing-work-queue/), it occurred to me that once the queue is empty, the Job object will terminate and subsequently, even if we add new work to the queue, the Job object will not restart. 

Trolling the internet for a solution, I came across [this](https://stackoverflow.com/a/49619517/1182202) which suggested terminating the workers with a failed status so that the Job controller keeps producing new ones. I feel this was horrible.

The fundamental issue with WebConsoles is that they have state i.e. The moment I start a console and put some Python in it, its a pet and not a cattle anymore. Kuberneted does not like pets. All the pods are cattle in that you can kill a random one - something you cannot do with consoles.

The thought crossed my mind that maybe we need to move to an architecture in which we keep the state of consoles separate from the workers i.e. when I type "print(a)" into my console, it will push this line to my context, take this context to a vanilla worker that will evaluate the entire context and return the results.

This has the obvious issue that as my code grows, my worker has to do more and more repeated work. We can probably make clever use of an LRU cache to avoid this but this would mean figuring out a way to serialise the InteractiveConsole object with all its state.

If we can do this, it will make the worker architcture super-simple b/c none of the workers will have state. That said, there is still the issue with persistent storage. How do we let our users save their sessions along with other files e.g. CSVs?

Another possible solution is give up on this approach of trying to shoehorn what is a pet to be a cattle and use [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/). This still leaves us with the problem of how are we going to provision Pods in a StatefulSet (to run WebConsoles) from within the application. It turns out [this is possible](https://kubernetes.io/docs/tasks/administer-cluster/access-cluster-api/#accessing-the-api-from-a-pod).
