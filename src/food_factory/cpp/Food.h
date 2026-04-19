/*
 * Food.h
 *
 *  Created on: Mar 10, 2021
 *      Author: som
 */

#ifndef FOOD_H_
#define FOOD_H_
#include <string>

using namespace std;

class Food {
public:
    virtual string getName() = 0;

    virtual ~Food(){

    }
};


#endif /* FOOD_H_ */
