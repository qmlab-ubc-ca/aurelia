.. toctree::
   :maxdepth: 1

.. _derivations:

Derivations
***********

Band Structure
==============

The tight-binding dispersions for the following lattices are given. The :math:`E_\text{nn}` term is added if ``self.warp = "on"``

.. math::

    \begin{equation}
        \begin{split}
            \text{Square}: \quad E_\text{n}&=E_0+2t[\cos(k_x a)+\cos(k_y a)]\\
            \quad E_\text{nn}&=rt[\cos(2k_x a)+\cos(2k_y a)]\\
            \text{Rectangle}: \quad E_\text{n}&=E_0+2t_1\cos(k_x a)+2t_2\cos(k_y b)]\\
            \quad E_\text{nn}&=E_0+rt_1\cos(2k_x a)+rt_2\cos(2k_y b)\\
            \text{Hexagonal}: \quad E_\text{n}&=E_0+2t[\cos(a/2(k_x+\sqrt{3}ky))+\\
            &\quad\quad\cos(a/2(k_x-\sqrt{3}ky))+\cos(k_x a)]\\
            \quad E_\text{nn}&=E_0+2rt[\cos(a/2(3k_x+\sqrt{3}ky))+\\
            &\quad\quad\cos(a/2(\sqrt{3}ky)-3kx)+\cos(\sqrt{3}k_y a)]\\
            \text{Honeycomb}: \quad E_\text{n}&=E_0\pm \\
            &\quad\quad t\sqrt{3+2\cos(\sqrt{3}k_x a)+4\cos(\sqrt{3}k_x a/2)\cos(3k_y a/2)}\\
            \quad E_\text{nn}&=2rt[\cos(a/2(\sqrt{3}k_x+3k_y))+\\
            &\quad\quad\cos(a/2(\sqrt{3}k_x-3k_y))+\cos(a\sqrt{3}k_x)]\\
        \end{split}
    \end{equation}

Matrix elements
===============

If ``ME["type"] = "symm"``: The matrix elements the same symmetry as that of the tight-binding model, in that they are periodic in $k$-space in the same way. The equations are:

.. math::
    \begin{equation}
        \begin{split}
            \text{Square}: \quad M_n&=t[\cos(k_x a)+\cos(k_y a)]+P(k_x, k_y)\\
            \text{Rectangle}: \quad M_n&=t_1\cos(k_x a)+2t_2\cos(k_y b)]+P(k_x, k_y)\\
            \text{Hexagonal}: \quad M_n&=t[\cos(a/2(k_x+\sqrt{3}ky))+\\
            &\quad\quad\cos(a/2(k_x-\sqrt{3}ky))+\cos(k_x a)]+P(k_x, k_y)\\
            \text{Honeycomb}: \quad M_n&=t\sqrt{3+2\cos(\sqrt{3}k_x a)+4\cos(\sqrt{3}k_x a/2)\cos(3k_y a/2)}+P(k_x, k_y)\\
        \end{split}
    \end{equation}

Here, if ``Bands.symmetry = "custom"`` from imported bands, then this mode does not do anything.

If ``ME["type"] = "rot"``: The matrix elements give rotational symmetry, which mimics the orbital selectivity of linear and/or circularly polarized light. Here, 

.. math::

    \begin{equation}
        \phi = \arctan\left(\frac{k_y}{k_x}\right), \quad M_\text{rot} = \cos(n\phi)
    \end{equation}

If this mode is selected, then :math:`n` (specified in the field ``ME["rotN"]``) gives the order of rotational symmetry. If ``ME["rotN"]`` is not specified, then the order is randomly selected according to the rotational symmetry of the lattice defined in the tight-binding model:
    
- Rectangle: :math:`n = 1, 2`
- Square: :math:`n = 1, 2, 4`
- Hexagonal/Honeycomb: :math:`n = 1, 2, 3, 6`

    
If ``ME["type"] = "rot"``: The matrix elements are given by a random polynomial. If this mode is selected, then the field ``ME["polyN"]`` gives the order of the polynomial. If ``ME["polyN"]`` is not specified, then the order is randomly selected.

Self-energy
===========

1. Fermi-liquid self-energy

  - Real part: :math:`\Sigma' = 0`

  - Imaginary part: :math:`\Sigma'' = D \, \omega^2 + \Sigma_0`

  - Dictionary keys:

    - ``SE["val"]`` = :math:`D`
    - ``SE["ImS0"]`` = :math:`\Sigma_0`

  - Default values (if not provided):

    - :math:`\Sigma_0 = 0.01`      
    - :math:`D \in [0.05, 0.25]`.

2. Electron-boson kink self-energy
The self-energy is phenomenological:

  .. math::

      \Sigma'(\omega) &= R \left[ \frac{\gamma}{(\omega + \omega_0)^2 + \gamma^2}
          - \frac{\gamma}{(\omega - \omega_0)^2 + \gamma^2} \right] \\
      \Sigma''(\omega) &= \Sigma_1 - \frac{\Sigma_1 - \Sigma_0}{1 + e^{-(\omega + \omega_0)\gamma}}

  - Dictionary keys and initialized random values (if not provided):

    - ``SE["Amp"]`` = :math:`R \in [0, 0.01]`
    - ``SE["Ekink"]`` = :math:`\omega_0 \in [0.05, 0.3]`
    - ``SE["gamma"]`` = :math:`\gamma \in [0, 50]`
    - ``SE["ImS0"]`` = :math:`\Sigma_0 \in [0.015, 0.025]`
    - ``SE["ImS1"]`` = :math:`\Sigma_1 \in [0.115, 0.125]`

Photoemission intensity
=======================

The spectral function and matrix elements are calculated at once using ``S.Make_specfun(m)``. Depending on the dimension of the calculation: 

.. math::

  \text{cube:}\quad 
  I(k_x, k_y, \omega) = \sum_m M_m(\omega)\frac{\Sigma_m''(\omega)}{(\omega-\epsilon_\mathbf{k}-\Sigma'_m(\omega))^2+\Sigma''_m(\omega)^2}

.. math::

  \text{sliceEk:}\quad 
  I(k_x, k_{y_0}, \omega) = \sum_m M_m(\omega)\frac{\Sigma_m''(\omega)}{(\omega-\epsilon_\mathbf{k}-\Sigma'_m(\omega))^2+\Sigma''_m(\omega)^2}

.. math::

  \text{slicekk:}\quad 
  I(k_x, k_y) = \sum_m \int_{\Delta\omega} M_m(\omega)\frac{\Sigma_m''(\omega)}{(\omega-\epsilon_\mathbf{k}-\Sigma'_m(\omega))^2+\Sigma''_m(\omega)^2} d\omega

where :math:`\Delta\omega = k_B T + \Delta E`

Then, ``S.Make_specmod(m)`` adds the Fermi-Dirac distribution and resolution broadening.  

The Fermi-Dirac is added by multiplication:

.. math::

  I_\text{FD}(\mathbf{k}, \omega) &= f_\text{FD}(\omega, T) I(k_x, k_y, \omega), \\
  f_\text{FD}(\omega, T) &= \frac{1}{1 + e^{\omega - E_F / k_B T}}

The resolution effects are added by convolving :math:`I_\text{FD}(k_x, k_y, \omega)` in energy and momenta with Gaussian functions whose full-width-half-max are defined by :math:`\Delta E` and :math:`\Delta k`, respectively:

.. math::

  I_\text{res}(\mathbf{k}, \omega) = G(\Delta k, k_x, k_y) \ast 
  \big(G(\Delta E, \omega) \ast I_\text{FD}(\mathbf{k}, \omega)\big)

The probe photon energy
=======================

For real values of ``theta`` and ``alpha`` (i.e., for the photoelectron to be emitted), the condition

.. math::

    E_k = h \nu - \Phi - E_b \geq \frac{\hbar^2 (k_x^2 + k_y^2)}{2 m_e}

must be satisfied for the deepest binding energies and largest momenta. This gives:

.. math::

    h \nu \geq \frac{\hbar^2 k_\text{lim}^2}{m_e} + \min(\omega) + \Phi

To ideally collect angles within ~45°, we add a factor of 2 to the RHS and a random number ``r`` in [0,5] eV:

.. math::

    h \nu = \frac{2 \hbar^2 k_\text{lim}^2}{m_e} + \min(\omega) + \Phi + r

The momentum-to-angle conversion
================================

We define the sample's out-of-plane direction as :math:`\hat{z}`.  
The axis parallel (perpendicular) to the slit of the hemispherical analyzer is denoted :math:`\hat{y}` (:math:`\hat{x}`).  

- The polar angle :math:`\theta` is a rotation about the :math:`\hat{y}` axis.  
- The tilt angle :math:`\phi` is a rotation about the :math:`\hat{x}` axis.  
- The azimuth angle :math:`\alpha` is a rotation about the :math:`\hat{z}` axis.  

The angles :math:`\theta` and :math:`\alpha` are calculated from conservation of momentum:

.. math::

    \theta = \text{sign}(k_x)\arcsin\left(\frac{\hbar\sqrt{k_x^2+k_y^2}}{\sqrt{2m_eE_k}}\right),
    \quad\quad
    \alpha = \arcsin\left(\frac{\hbar k_y}{\sqrt{2m_eE_k}\sin\theta}\right)

The vector defining the direction of photoelectron propagation is:

.. math::

    \begin{equation}
    \begin{split}
        d'&=R(\alpha, \hat{z})R(\theta, \hat{y})d\\
        &=\begin{pmatrix}
                \cos\alpha\cos\theta & -\sin\alpha & \cos\alpha\sin\theta \\
                \sin\alpha\cos\theta & \cos\alpha &  \sin\alpha\sin\theta\\
                -\sin\theta & 0 & \cos\theta\\
        \end{pmatrix}
        \begin{pmatrix}
                0 \\
                0 \\
                1 \\
        \end{pmatrix}
        =\begin{pmatrix}
                \cos\alpha\sin\theta \\
                \sin\alpha\sin\theta \\
                \cos\theta \\
        \end{pmatrix}\\
    \end{split}    
    \end{equation}

To get the emission angles with respect to the analyzer, we find the angles :math:`\theta_m` and :math:`\phi_m` needed to map :math:`d'` onto :math:`d`.  
We rotate first along the analyzer slit (:math:`\theta_m`), then perpendicular to it (:math:`\phi_m`):

.. math::

    \begin{equation}
    \begin{split}
        d&=R(\phi_m, \hat{x})R(\theta_m, \hat{y})d'\\
        \begin{pmatrix}
                0 \\
                0 \\
                1 \\
        \end{pmatrix}
        &=\begin{pmatrix}
                \cos\theta_m & 0 & \sin\theta_m\\
                \sin\phi_m\sin\theta_m & \cos\phi_m & -\sin\phi_m\cos\theta_m \\
                -\cos\phi_m\sin\theta_m & \sin\phi_m &  \cos\phi_m\cos\theta_m \\            
        \end{pmatrix}
        \begin{pmatrix}
                d'_x \\
                d'_y \\
                d'_z \\
        \end{pmatrix}\\
    \end{split}    
    \end{equation}

Adding offset angles is straightforward:  
we apply the rotation matrices :math:`R(\theta_0,\hat{y})` and :math:`R(\phi_0,\hat{x})` to :math:`d` before calculating the photoemission angles:

.. math::

    d' = R(\alpha, \hat{z})R(\theta, \hat{y})R(\phi_0,\hat{x})R(\theta_0,\hat{y})d

This leads to the system of equations:

.. math::

    \theta_m = -\arctan\left(\frac{d'_x}{d'_z}\right), \qquad
    \phi_m = \arcsin(d'_y)

Alternatively, if we rotate perpendicular to the slit first, then along the slit, we reverse the order of the matrices:

.. math::

    d = R(\theta_m, \hat{y})R(\phi_m, \hat{x})d'

In this case:

.. math::

    \theta_m = -\arcsin(d'_x), \qquad
    \phi_m = \arctan\left(\frac{d'_y}{d'_z}\right)

Having obtained this conversion for all :math:`k_x` and :math:`k_y`,  
we define a square mesh of angles :math:`\theta_M` and :math:`\phi_M` and interpolate onto it using  
:math:`(\theta_m, \phi_m, I_\text{res}(\mathbf{k},\omega))`.  

The resulting values :math:`I(\theta, \phi, E_k)` are stored in ``arpes.intensity``.  

When simulating a sample with flake-like domains at different offset angles, the conversion is done for each domain.  
In this case, the function returns the intensity :math:`I(\theta, \phi, E_k, \theta_0, \phi_0)` directly, so intensity from all flakes can be combined externally.  

The angle-to-momentum check
===========================
To convert from angle to momentum, we simply define a transformation matrix :math:`T` consisting of all the rotational matrices:

.. math::

    \begin{equation}
        \begin{split}
            T&=R_\text{motors}(\theta_m, \phi_m)R_\text{offset}(\theta_0, \phi_0, \alpha_0)\\
            &=R(\theta_m, \hat{y})R(\phi_m, \hat{x})R(\theta_0,\hat{y})R(\phi_0,\hat{x})R(\alpha_0,\hat{z})
        \end{split}
    \end{equation}

Then the normalized vector for photoelectron :math:`k_\text{norm}` is given by solving :math:`Tk_\text{norm}=d`

.. math::


    \begin{equation}
        k= |k|T/d,
    \end{equation}

where :math:`d=(0,0,1)`, and :math:`|k|=\sqrt{2m_e E_k}\hbar`.