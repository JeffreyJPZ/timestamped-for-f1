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
 *  Superclass for subclasses that use weighted dimensions.
 *
 *     Any child classes should implement DistanceFunction and override 
 *
 *     distance() and distanceToRect().
 */
public abstract class WeightedDistanceFunction implements DistanceFunction {

	private double[] weights;
	
	// Constructor. Loads weights.
	public WeightedDistanceFunction(double[] weights) {
		setWeights(weights);
	}
	
	// Unweighted constructor, just in case the user forgets to specify weights.
	//  Loads the failover 1.0 weights from setWeights().
	public WeightedDistanceFunction() {
		setWeights(null);
	}
	
	// Loads a new set of weights.  Default is a weight of 1.0 if passed bad data.
	public void setWeights(double[] weights) {
		if ( weights == null || weights.length == 0 ) {
			this.weights = new double[1];
			this.weights[0] = 1.0;
			return;
		}
		this.weights = weights;
	}
	
	// Returns the current set of weights.
	public double[] getWeights() {
		return this.weights;
	}
	
	// Returns the weight for the index-th dimension.  
	// Out of bounds requests return a weight of one.
	public double getWeight(int index)
	{
		if ( index < 0 || index >= weights.length ) {
			return 1.0;
		}
		return weights[index];
	}
	
	// Child classes override this!
	@Override
    public abstract double distance(double[] p1, double[] p2);
	
	// Child classes override this!
    @Override
    public abstract double distanceToRect(double[] point, double[] min, double[] max);
	
}
