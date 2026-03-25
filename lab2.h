//
// Created by ritokk on 03.03.26.
//

#ifndef LAB2_LAB2_H
#define LAB2_LAB2_H
struct Point {
    double x, y;
};
struct Triangle {
    Point A, B, C;
};

void distance(Point &P1, Point &P2, double &d);
void heronArea(Triangle &t, double &area);
void isTriangleReal(Triangle &t, bool &result);
void checkPointPositionVector(Point &p,Triangle &t);
void checkPointPositionByArea(Point &p,Triangle &t);
void startingPoint();
#endif //LAB2_LAB2_H