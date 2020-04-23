# pdf2markup

A script that converts (ppt-like) pdf to mark-up style text with headers and bullet points.

By default, it converts the first line on each page to a 5th level header, and retains certain bullet point structures (probably needs to be adjusted based on the file). 

It can be run from the command line, with two options:
1. automatic output: enter filename, (password), skip unwanted lines if they contain specific characters (e.g., page label "3 / 10", name of the presenter),  and whether you want to modify the text formatting (merge lines broken up by a narrow column and change special characters to bullet point "-"). It then outputs the processed result for the entire pdf file.
2. manual specification: enter the parameters above for each page, check output, and continue to next page if you're satisfied with the output.

I use it to get my pdf lecture slides into markup-enabled notebooks (e.g., Simplenote). 

Example output:

##### Output system
 - controls contraction of skeletal muscles
 - autonomic nervous system: 
1. Spinal cord and brainstem circuits
- Reflexive or voluntary movement (“final common path”)
- Coordination between different muscle groups, even with isolated spinal cord
2. Upper motor neurons
- Cell bodies in brainstem or cortex, synapses to local circuit neurons or lower motor neurons
- Cortex: Initiation of voluntary movements, complex spatio-temporal sequences of skilled movements
- Brainstem: regulation of muscle tone, orienting 3-4 Basal ganglia and cerebellum
- No direct access to local circuit neurons or lower motor neurons
- Cerebellum: attenuation of motor error (real-time and long-term)
- Basal ganglia: movement initiation
