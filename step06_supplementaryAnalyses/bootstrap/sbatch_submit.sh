#!/bin/bash
for rand_ind in {1..500}
do
    echo "rand index: $rand_ind"
	sbatch -J ${rand_ind} \
		-o log/out.${rand_ind}.txt \
		-e log/error.${rand_ind}.txt \
		submit_Step_1st.sh $rand_ind
done
