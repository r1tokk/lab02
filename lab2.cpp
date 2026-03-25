//
// Created by ritokk on 03.03.26.
//
#include "lab2.h"
#include <cmath>
#include <iostream>

using namespace std;

void distance(Point &P1, Point &P2, double &d) {
    d = sqrt(pow(P1.x - P2.x, 2) + pow(P1.y - P2.y, 2));
}
void heronArea(Triangle &t, double &area) {
    double a = 0.0, b = 0.0, c = 0.0;
    distance(t.A, t.B, a);
    distance(t.B, t.C, b);
    distance(t.C, t.A, c);
    double halfP = (a + b + c) / 2;

    area = sqrt(halfP * (halfP - a) * (halfP  - b) * (halfP - c));
}
void isTriangleReal(Triangle &t, bool &result) {
    double area = 0.0;
    heronArea(t, area);
    result = (area > 1e-9);
}
void crossProduct(Point &a, Point &b, Point &c, double &result) {
    result = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}
void checkPointPositionVector(Point &p,Triangle &t) {
    double cp1, cp2, cp3;
    crossProduct(t.A, t.B, p, cp1);
    crossProduct(t.B, t.C, p, cp2);
    crossProduct(t.C, t.A, p, cp3);

    bool all_pos = (cp1 > 1e-9) || (cp2 > 1e-9) || (cp3 > 1e-9);
    bool all_neg = (cp1 < -1e-9) || (cp2 < -1e-9) || (cp3 < -1e-9);

    if (all_pos && all_neg) {
        cout << "Точка знаходиться ззовні трикутнику (За методом векторного добутку)" << endl;
    }
    else if (cp1 == 0 || cp2 == 0 || cp3 == 0) {
        cout << "Точка знаходиться на стороні трикутника (За методом векторного добутку)" << endl;
    }
    else {
        cout << "Точка знаходиться всередині трикутника (За методом векторного добутку)" << endl;
    }
}
void checkPointPositionByArea(Point &p,Triangle &t) {
    double area_main = 0.0;
    double area_1 = 0.0;
    double area_2 = 0.0;
    double area_3 = 0.0;

    Triangle t1 = {t.A, t.B, p};
    Triangle t2 = {t.B, t.C, p};
    Triangle t3 = {t.C, t.A, p};

    heronArea(t, area_main);
    heronArea(t1, area_1);
    heronArea(t2, area_2);
    heronArea(t3, area_3);

    double area_sum = area_1 + area_2 + area_3;
    if (fabs(area_main - area_sum) < 1e-9) {
        if (area_1 < 1e-9 || area_2 < 1e-9 || area_3 < 1e-9) {
            cout << "Точка знаходиться на стороні трикутника (За методом площі)" << endl;
        } else {
            cout << "Точка знаходиться всередині трикутника (За методом площі)" << endl;
        }
    } else {
        cout << "Точка знаходиться ззовні трикутника (За методом площі)" << endl;
    }

}
void startingPoint() {
    Triangle t{};

    cout << "Введіть координати вершини A (x y): ";
    cin >> t.A.x >> t.A.y;
    cout << "Введіть координати вершини B (x y): ";
    cin >> t.B.x >> t.B.y;
    cout << "Введіть координати вершини C (x y): ";
    cin >> t.C.x >> t.C.y;

    bool real;
    isTriangleReal(t, real);
    if (!real) {
        cout << "Трикутник є виродженим" << endl;
       return;
    }
    int n;
    cout << "Введіть кількість точок які ви хочете перевірити: ";
    cin >> n;
    if (n <= 0) {
        cout << "Кількість точок має бути більшою за нуль.\n";
        return;
    }
    for (int i = 0; i < n; i++) {
        Point p = {0,0};
        cout << "Введіть координати точки " << i + 1 << " (x y): ";
        cin >> p.x >> p.y;

        checkPointPositionVector(p, t);
        checkPointPositionByArea(p, t);
    }
}