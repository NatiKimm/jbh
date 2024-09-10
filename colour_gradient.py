import random
import math
from matplotlib import pyplot, cm
from time import time
import numpy as np

# Generate a chaotic attractor with color interpolation over time
def search_attractors_with_color_gradient(n=1):
    found = 0
    while found < n:
        # Random starting point
        x = random.uniform(-0.5, 0.5)
        y = random.uniform(-0.5, 0.5)

        # Random alternative point nearby
        xe = x + random.uniform(-0.5, 0.5) / 1000
        ye = y + random.uniform(-0.5, 0.5) / 1000

        # Distance between the two points
        dx = xe - x
        dy = ye - y
        d0 = math.sqrt(dx * dx + dy * dy)

        # Random parameter vector
        a = [random.uniform(-2, 2) for i in range(12)]

        # Lists to store the entire path, trajectory
        x_list = [x]
        y_list = [y]

        converge = False
        lyapunov = 0

        # Iteratively pass (x, y) into the quadratic map
        for i in range(10000):
            # Compute next point (using the quadratic map)
            xnew = a[0] + a[1] * x + a[2] * x * x + a[3] * y + a[4] * y * y + a[5] * x * y
            ynew = a[6] + a[7] * x + a[8] * x * x + a[9] * y + a[10] * y * y + a[11] * x * y

            # Check if we converge to infinity
            if xnew > 1e10 or ynew > 1e10 or xnew < -1e10 or ynew < -1e10:
                converge = True
                break

            # Check if we converge to a single point
            if abs(x - xnew) < 1e-10 and abs(y - ynew) < 1e-10:
                converge = True
                break

            # Check for chaotic behavior
            if i > 1000:
                # Compute next alternative point
                xenew = a[0] + a[1] * xe + a[2] * xe * xe + a[3] * ye + a[4] * ye * ye + a[5] * xe * ye
                yenew = a[6] + a[7] * xe + a[8] * xe * xe + a[9] * ye + a[10] * ye * ye + a[11] * xe * ye

                # Compute the distance between the new points
                dx = xenew - xnew
                dy = yenew - ynew
                d = math.sqrt(dx * dx + dy * dy)

                # Lyapunov exponent
                lyapunov += math.log(abs(d / d0))

                # Rescale the alternative point
                xe = xnew + d0 * dx / d
                ye = ynew + d0 * dy / d

            # Update (x, y)
            x = xnew
            y = ynew

            # Store (x, y) in our path lists
            x_list.append(x)
            y_list.append(y)

        # Check if chaotic behavior has been found
        if not converge and lyapunov >= 10:
            # Update counter and print message
            found += 1
            print("Found another strange attractor with Lyapunov exponent = " + str(lyapunov) + "!")

            # Prepare color interpolation
            t = np.linspace(0, 1, len(x_list[100:]))  # Normalized time
            colors = cm.plasma(t)  # Use a color map, 'plasma'

            # Clear figure
            pyplot.style.use("dark_background")
            pyplot.axis("off")

            # Create the plot with interpolated colors
            pyplot.scatter(x_list[100:], y_list[100:], s=0.5, c=colors, linewidth=0)

            # Save the figure
            name = f"pictures/attractor_gradient_{time()}.png"
            pyplot.savefig(name, dpi=500)
            pyplot.close()
            return name
