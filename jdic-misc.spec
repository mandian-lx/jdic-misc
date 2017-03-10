%{?_javapackages_macros:%_javapackages_macros}

%define subversion 1736
%define libname %(tr \- \_ <<< %name )

Summary:	The JDesktop Integration Components (JDIC) - misc inbubator
Name:		jdic-misc
Version:	0.9.4r%{subversion}svn
Release:	1
License:	LGPLv2.1
Group:		Development/Java
URL:		http://javadesktop.org/articles/jdic/index.html#jdic
# svn checkout https://svn.java.net/svn/jdic~svn/trunk/src/incubator/misc/ jdic-misc-code
# cp -far jdic-misc-code jdic-misc-0.9.4r1736svn
# find jdic-misc-0.9.4r1736svn -name \.svn -type d -exec rm -fr ./{} \; 2> /dev/null
# tar Jcf jdic-misc-0.9.4r1736svn.tar.xz jdic-misc-0.9.4r1736svn
Source0:	%{name}-%{version}.tar.xz
# Adapted from https://svn.java.net/svn/jdic~svn/trunk/src/incubator/tray/src/unix/native/jni/Makefile
Source1:	Makefile.jdic-misc

BuildRequires:	jpackage-utils
BuildRequires:	ant
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(xt)

Requires:	jpackage-utils
Requires:	java-headless
Requires:	libx11

%description
The JDesktop Integration Components (JDIC) project aims to make Java™
technology-based applications ("Java applications") first-class citizens of
current desktop platforms without sacrificing platform independence.

JDIC provides Java applications with access to facilities provided by the
native desktop such as the mailer, the browser, and registered document
viewing applications. Additionally it provides the mechanisms by which Java
applications can integrate into the native desktop such as registering Java
applications as document viewers on the desktop, creating tray icons on the
desktop and creating installer packages.

JDIC consists of a collection of Java packages (JDIC API), all with the
package name prefix org.jdesktop.jdic, and a JNLP application packaging tool
(JDIC Packager).

This package containt the misc incubator

%files
%{_jnidir}/%{name}*.jar
%{_libdir}/%{libname}/*so
%doc README

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
BuildArch:	noarch

%description javadoc
API documentation for %{name}.

%files javadoc
%{_javadocdir}/%{name}

#----------------------------------------------------------------------------

%prep
%setup -q
# Delete all prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete
find . -name "*.so" -delete

cp %{SOURCE1} src/linux/native/jni/Makefile

# Fix paths
sed -i -e '{
	     s|\${src.dir}/unix|\${src.dir}/linux|g
	     s|<copy file="${unix.native.jni.dir}/libjdic_misc.so" todir="${dist.dir}" />|<copy todir="${dist.dir}"><fileset dir="${unix.native.jni.dir}" includes="*.so" /></copy>|g
	   }' build.xml

%build
export ANT_OPTS="-Dfile.encoding=ISO-8859-1 -Dtarget.version=1.7 -Dtarget.source=1.7"
%setup_compile_flags
%ant buildall

# add the index to the jars
%jar i dist/linux/%{libname}.jar

%install
# jars
install -dm 0755 %{buildroot}%{_jnidir}/
install -pm 0644 dist/linux/%{libname}.jar %{buildroot}%{_jnidir}/%{name}.jar

# native lib
install -dm 0755 %{buildroot}%{_libdir}/%{libname}/
install -pm 0644 dist/linux/*.so %{buildroot}%{_libdir}/%{libname}/

# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr dist/linux/javadoc/* %{buildroot}%{_javadocdir}/%{name}

