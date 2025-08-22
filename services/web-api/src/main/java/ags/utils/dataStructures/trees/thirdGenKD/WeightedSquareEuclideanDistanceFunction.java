/**
 * Copyright (c) 2012 tkiesel
 * 
 * This software is provided 'as-is', without any express or implied
 * warranty. In no event will the authors be held liable for any damages
 * arising from the use of this software.
 * 
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 * 
 * 1. The origin of this software must not be misrepresented; you must not
 *    claim that you wrote the original software. If you use this software
 *    in a product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. This notice may not be removed or altered from any source distribution.
 *
 */

package ags.utils.dataStructures.trees.thirdGenKD;

/**
 *
 */
public class WeightedSquareEuclideanDistanceFunction extends WeightedDistanceFunction implements DistanceFunction {
	
	// Constructor. Loads weights.
	public WeightedSquareEuclideanDistanceFunction(double[] weights) {
		super(weights);
	}
	
	// Unweighted constructor, just in case the user forgets to specify weights.
	// In this failover case, this DistanceFunction should give identical results as EuclideanDistanceFunction
	public WeightedSquareEuclideanDistanceFunction() {
		super();
	}

    @Override
    public double distance(double[] p1, double[] p2) {
        double d = 0;

        for (int i = 0; i < p1.length; i++) {
            double diff = getWeight(i)*(p1[i] - p2[i]);
            d += diff * diff;
        }

        return d;
    }

    @Override
    public double distanceToRect(double[] point, double[] min, double[] max) {
        double d = 0;

        for (int i = 0; i < point.length; i++) {
            double diff = 0;
            if (point[i] > max[i]) {
                diff = getWeight(i)*(point[i] - max[i]);
            }
            else if (point[i] < min[i]) {
                diff = getWeight(i)*(point[i] - min[i]);
            }
            d += diff * diff;
        }

        return d;
    }
}
